"""TikTok canlı yayın bağış animasyonları sunucusu.

TikTok canlı yayınındaki hediye / beğeni / takip / yorum olaylarını dinler ve
WebSocket üzerinden tarayıcıdaki overlay sayfasına iletir. Overlay sayfası
OBS veya TikTok Live Studio'ya "tarayıcı kaynağı" olarak eklenir.

Çalıştırma:
    python -m live_overlay.server --user kullanici_adi
    python -m live_overlay.server            # TikTok'suz, panelden test için
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import store

STATIC_DIR = Path(__file__).parent / "static"
MODES = ("halay", "race", "taki", "tug", "karpuz")
HTML_PREFIX = '<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
# Overlay kütüphaneleri internetten değil yerel kopyadan yüklenir: CDN erişilemese de sahne açılır.
CDN_TO_LOCAL = {
    "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js": "vendor/three.min.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js": "vendor/GLTFLoader.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/utils/SkeletonUtils.js": "vendor/SkeletonUtils.js",
}

settings: dict[str, Any] = store.load_settings(MODES)
ledger = store.Ledger()


class Hub:
    """Bağlı overlay/panel istemcilerini ve ortak durumu tutar."""

    def __init__(self) -> None:
        self.clients: set[WebSocket] = set()
        self.mode: str = MODES[0]
        self.tiktok_user: str = ""
        self.tiktok_status: str = "disconnected"  # disconnected | connecting | connected | error
        self.tiktok_error: str = ""
        self.stats: dict[str, Any] = {}  # overlay'in bildirdiği kare hızı ve kalite
        self.step = 0                    # otomatik programda kaçıncı adım
        self.left = 0                    # adımın bitmesine kalan saniye

    def state(self) -> dict[str, Any]:
        return {
            "type": "state",
            "mode": self.mode,
            "modes": list(MODES),
            "tiktok": {
                "user": self.tiktok_user,
                "status": self.tiktok_status,
                "error": self.tiktok_error,
            },
            "settings": settings,
            "program": self.program(),
            "stats": self.stats if time.time() - self.stats.get("ts", 0) < 10 else {},
        }

    def program(self) -> Optional[dict[str, Any]]:
        steps = settings["program"]
        if not settings["program_on"] or len(steps) < 2:
            return None
        return {"next": steps[(self.step + 1) % len(steps)]["mode"], "sec": max(0, self.left)}

    def start_program(self) -> None:
        """Programı, şu an açık olan modun adımından başlatır."""
        steps = settings["program"]
        self.step = next((i for i, st in enumerate(steps) if st["mode"] == self.mode), 0)
        self.mode = steps[self.step]["mode"]
        self.left = steps[self.step]["min"] * 60

    async def broadcast(self, message: dict[str, Any]) -> None:
        data = json.dumps(message, ensure_ascii=False)
        dead = []
        for ws in list(self.clients):
            try:
                await ws.send_text(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.clients.discard(ws)

    async def set_status(self, status: str, error: str = "") -> None:
        self.tiktok_status = status
        self.tiktok_error = error
        await self.broadcast(self.state())


hub = Hub()


async def emit(event: dict[str, Any]) -> None:
    """Bir izleyici olayını denetler, deftere işler ve overlay'e yollar."""
    user = event.get("user")
    if user:
        if user["id"] in settings["gizli"]:
            user["name"], user["avatar"] = store.SAFE_NAME, ""
        else:
            user["name"] = store.clean_name(user["name"], settings["yasak"])
    kind = event["type"]
    if kind == "gift" and user:
        user["alltime"] = ledger.add_gift(user, event["gift"], event["total"], hub.mode)  # önceki yayınlardaki toplamı
    else:
        ledger.count(kind, int(event.get("count", 1)) if kind == "like" else 1)
    await hub.broadcast(event)


# ---------------------------------------------------------------------------
# TikTok bağlantısı
# ---------------------------------------------------------------------------


def _first_url(image: Any) -> str:
    """TikTok ImageModel nesnesinden ilk URL'yi güvenli şekilde alır."""
    if image is None:
        return ""
    for attr in ("m_urls", "url_list", "urls"):
        urls = getattr(image, attr, None)
        if urls:
            return str(urls[0])
    return ""


def _user(user: Any) -> dict[str, str]:
    if user is None:
        return {"id": "anon", "name": "Anonim", "avatar": ""}
    unique_id = getattr(user, "unique_id", "") or getattr(user, "display_id", "") or ""
    name = getattr(user, "nickname", "") or getattr(user, "nick_name", "") or unique_id or "Anonim"
    return {
        "id": str(unique_id or getattr(user, "id", "") or name),
        "name": str(name),
        "avatar": _first_url(getattr(user, "avatar_thumb", None)),
    }


class TikTokBridge:
    """TikTokLive istemcisini yönetir, olayları ortak biçime çevirir."""

    RETRY_SECONDS = 15

    def __init__(self) -> None:
        self._task: Optional[asyncio.Task] = None
        self._client: Any = None
        # Seri (combo) hediyelerde aynı hediye artan repeat_count ile tekrar
        # gelir; yalnızca farkı iletmek için son sayıyı saklarız.
        self._streaks: dict[tuple, tuple[int, float]] = {}

    async def start(self, username: str) -> None:
        await self.stop()
        hub.tiktok_user = username.lstrip("@").strip()
        self._task = asyncio.create_task(self._run(hub.tiktok_user))

    async def stop(self) -> None:
        task, self._task = self._task, None
        if task:
            task.cancel()
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass
        await self._close_client()
        self._streaks.clear()
        await hub.set_status("disconnected")

    async def _close_client(self) -> None:
        client, self._client = self._client, None
        if client is not None:
            try:
                await client.disconnect()
            except Exception:
                pass

    async def _run(self, username: str) -> None:
        try:
            from TikTokLive import TikTokLiveClient
            from TikTokLive.events import (
                CommentEvent,
                ConnectEvent,
                FollowEvent,
                GiftEvent,
                LikeEvent,
                ShareEvent,
            )
        except ImportError:
            await hub.set_status("error", "TikTokLive kurulu değil: pip install TikTokLive")
            return

        sign_key = os.environ.get("TIKTOK_SIGN_API_KEY", "")
        if sign_key:  # imza servisinin ücretli anahtarı: yoğun kullanımda bağlantı sınırına takılmamak için
            try:
                from TikTokLive.client.web.web_settings import WebDefaults

                WebDefaults.tiktok_sign_api_key = sign_key
            except Exception:
                pass

        while True:
            await hub.set_status("connecting")
            client = TikTokLiveClient(unique_id=f"@{username}")
            self._client = client

            @client.on(ConnectEvent)
            async def _on_connect(_event: Any) -> None:
                await hub.set_status("connected")

            @client.on(GiftEvent)
            async def _on_gift(event: Any) -> None:
                await self._handle_gift(event)

            @client.on(LikeEvent)
            async def _on_like(event: Any) -> None:
                await emit({"type": "like", "user": _user(event.user), "count": max(1, int(getattr(event, "count", 1) or 1))})

            @client.on(FollowEvent)
            async def _on_follow(event: Any) -> None:
                await emit({"type": "follow", "user": _user(event.user)})

            @client.on(ShareEvent)
            async def _on_share(event: Any) -> None:
                await emit({"type": "share", "user": _user(event.user)})

            @client.on(CommentEvent)
            async def _on_comment(event: Any) -> None:
                await emit({"type": "comment", "user": _user(event.user), "text": str(getattr(event, "comment", "") or "")[:200]})

            error = ""
            try:
                # connect() yayın bitene / bağlantı kopana kadar bekler.
                await client.connect()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # yayında değil, ağ hatası vb.
                if type(exc).__name__ == "UserOfflineError":
                    error = f"@{username} şu an canlı yayında değil. Yayın açılınca otomatik bağlanır."
                elif type(exc).__name__ == "UserNotFoundError":
                    error = f"@{username} bulunamadı. Kullanıcı adını kontrol edin."
                elif "ratelimit" in type(exc).__name__.lower() or "rate limit" in str(exc).lower():
                    error = "İmza servisi bağlantı sınırına takıldı. Birkaç dakika bekleyin ya da TIKTOK_SIGN_API_KEY ortam değişkenine anahtar girin."
                else:
                    error = f"{type(exc).__name__}: {exc}"[:300]
            finally:
                await self._close_client()

            await hub.set_status("error", error or "Bağlantı kapandı, yeniden deneniyor…")
            await asyncio.sleep(self.RETRY_SECONDS)

    async def _handle_gift(self, event: Any) -> None:
        gift = event.gift
        if gift is None:
            return
        user = _user(event.user)
        repeat = max(1, int(getattr(event, "repeat_count", 1) or 1))
        count = repeat

        if getattr(gift, "streakable", False):
            now = time.monotonic()
            key = (user["id"], getattr(event, "gift_id", 0) or getattr(gift, "id", 0), getattr(event, "group_id", 0))
            previous = self._streaks.get(key, (0, now))[0]
            count = repeat - previous
            if getattr(event, "repeat_end", 0):
                self._streaks.pop(key, None)
            else:
                self._streaks[key] = (repeat, now)
            # Bitiş olayı hiç gelmeyen eski serileri temizle.
            for stale in [k for k, (_, seen) in self._streaks.items() if now - seen > 120]:
                self._streaks.pop(stale, None)
            if count <= 0:
                return

        diamonds = max(1, int(getattr(gift, "diamond_count", 1) or 1))
        await emit(
            {
                "type": "gift",
                "user": user,
                "gift": {
                    "name": str(getattr(gift, "name", "") or "Hediye"),
                    "diamonds": diamonds,
                    "count": count,
                    "image": _first_url(getattr(gift, "image", None)) or _first_url(getattr(gift, "icon", None)),
                },
                "total": diamonds * count,
            }
        )


bridge = TikTokBridge()

# ---------------------------------------------------------------------------
# HTTP / WebSocket
# ---------------------------------------------------------------------------

app = FastAPI(title="TikTok Live Overlay", docs_url=None, redoc_url=None)
app.mount("/models", StaticFiles(directory=STATIC_DIR / "models"), name="models")  # 3B modeller
app.mount("/vendor", StaticFiles(directory=STATIC_DIR / "vendor"), name="vendor")  # three.js yerel kopyası


def _page(name: str) -> HTMLResponse:
    # Sayfalar gövde parçası olarak saklanır; doctype burada eklenir.
    body = (STATIC_DIR / name).read_text(encoding="utf-8")
    for cdn, local in CDN_TO_LOCAL.items():
        body = body.replace(cdn, local)
    boot = json.dumps(settings, ensure_ascii=False).replace("</", "<\\/")  # ayarlar sayfa açılmadan hazır olsun
    head = f"{HTML_PREFIX}<script>window.LIVE_SERVER=1;window.LIVE_SETTINGS={boot}</script>"
    return HTMLResponse(head + body, headers={"Cache-Control": "no-store"})


@app.get("/", response_class=HTMLResponse)
async def control_page() -> HTMLResponse:
    return _page("control.html")


@app.get("/overlay", response_class=HTMLResponse)
async def overlay_page() -> HTMLResponse:
    return _page("overlay.html")


@app.get("/api/state")
async def get_state() -> dict[str, Any]:
    return hub.state()


class ModeBody(BaseModel):
    mode: str


@app.post("/api/mode")
async def set_mode(body: ModeBody) -> dict[str, Any]:
    if body.mode not in MODES:
        raise HTTPException(400, f"Geçersiz mod. Seçenekler: {', '.join(MODES)}")
    hub.mode = body.mode
    if settings["program_on"]:
        hub.start_program()
    await hub.broadcast(hub.state())
    return hub.state()


@app.post("/api/reset")
async def reset() -> dict[str, bool]:
    """Yeni yayın: bu yayının toplamları 'tüm zamanlar'a eklenir, rapor arşivlenir, ekran sıfırlanır."""
    ledger.new_stream()
    await hub.broadcast({"type": "reset"})
    return {"ok": True}


@app.post("/api/round")
async def round_reset() -> dict[str, bool]:
    """Yalnızca açık olan turu baştan başlatır; sıralama ve toplamlar kalır."""
    await hub.broadcast({"type": "round"})
    return {"ok": True}


@app.get("/api/settings")
async def get_settings() -> dict[str, Any]:
    return settings


@app.post("/api/settings")
async def post_settings(body: dict[str, Any]) -> dict[str, Any]:
    was_on = settings["program_on"]
    settings.update(store.clean_settings(body, MODES, settings))
    store.save_settings(settings)
    if settings["program_on"] and not was_on:
        hub.start_program()
    await hub.broadcast({"type": "reload"})  # overlay yeni ayarlarla yeniden açılır; sıralama defterden geri gelir
    await hub.broadcast(hub.state())
    return settings


@app.get("/api/report")
async def report() -> dict[str, Any]:
    return ledger.report()


@app.get("/api/report.csv", response_class=PlainTextResponse)
async def report_csv() -> PlainTextResponse:
    return PlainTextResponse(ledger.report_csv(), media_type="text/csv; charset=utf-8", headers={"Content-Disposition": "attachment; filename=yayin-raporu.csv"})


@app.get("/api/tts")
async def tts(text: str = Query(min_length=1, max_length=120)) -> FileResponse:
    """Sesli anons: metni Türkçe seslendirir, aynı metni bir daha üretmemek için diske yazar."""
    if not settings["anons"]:
        raise HTTPException(404, "Sesli anons kapalı")
    try:
        import edge_tts
    except ImportError:
        raise HTTPException(503, "edge-tts kurulu değil: pip install edge-tts")
    path = store.DATA_DIR / "tts" / (hashlib.sha1(text.encode("utf-8")).hexdigest() + ".mp3")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            await asyncio.wait_for(edge_tts.Communicate(text, "tr-TR-AhmetNeural", rate="+8%").save(str(path)), timeout=8)
        except Exception as exc:
            path.unlink(missing_ok=True)
            raise HTTPException(502, f"Seslendirme yapılamadı: {type(exc).__name__}")
    return FileResponse(path, media_type="audio/mpeg")


class ConnectBody(BaseModel):
    user: str = Field(min_length=1, max_length=64)


@app.post("/api/connect")
async def connect(body: ConnectBody) -> dict[str, Any]:
    await bridge.start(body.user)
    return hub.state()


@app.post("/api/disconnect")
async def disconnect() -> dict[str, Any]:
    await bridge.stop()
    return hub.state()


class SimulateBody(BaseModel):
    type: str = "gift"
    name: str = Field(default="Test", max_length=40)
    gift: str = Field(default="Gül", max_length=40)
    diamonds: int = Field(default=1, ge=1, le=100000)
    count: int = Field(default=1, ge=1, le=1000)
    text: str = Field(default="", max_length=200)


@app.post("/api/simulate")
async def simulate(body: SimulateBody) -> dict[str, bool]:
    """Panelden test olayı gönderir (TikTok bağlantısı gerekmez)."""
    user: dict[str, Any] = {"id": "sim:" + body.name.lower(), "name": body.name, "avatar": ""}
    if body.type == "gift":
        event: dict[str, Any] = {
            "type": "gift",
            "user": user,
            "gift": {"name": body.gift, "diamonds": body.diamonds, "count": body.count, "image": ""},
            "total": body.diamonds * body.count,
        }
    elif body.type == "like":
        event = {"type": "like", "user": user, "count": body.count}
    elif body.type == "comment":
        event = {"type": "comment", "user": user, "text": body.text}
    elif body.type in ("follow", "share"):
        event = {"type": body.type, "user": user}
    else:
        raise HTTPException(400, "Geçersiz olay türü")
    await emit(event)
    return {"ok": True}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    hub.clients.add(ws)
    try:
        await ws.send_text(json.dumps(hub.state(), ensure_ascii=False))
        await ws.send_text(json.dumps(ledger.snapshot(), ensure_ascii=False))  # sıralamayı geri kur
        while True:
            raw = await ws.receive_text()
            try:  # overlay birkaç saniyede bir kare hızını bildirir
                msg = json.loads(raw)
                if msg.get("type") == "stats":
                    hub.stats = {"fps": float(msg.get("fps", 0)), "quality": str(msg.get("quality", ""))[:12], "ts": time.time()}
            except (ValueError, TypeError, AttributeError):
                pass
    except WebSocketDisconnect:
        pass
    finally:
        hub.clients.discard(ws)


async def _ticker() -> None:
    """Saniyede bir: defteri diske yazar ve otomatik programı ilerletir."""
    n = 0
    while True:
        await asyncio.sleep(1)
        n += 1
        if n % 3 == 0:
            ledger.save()
        steps = settings["program"]
        if settings["program_on"] and len(steps) > 1:
            hub.left -= 1
            if hub.left <= 0:
                hub.step = (hub.step + 1) % len(steps)
                hub.mode, hub.left = steps[hub.step]["mode"], steps[hub.step]["min"] * 60
                await hub.broadcast(hub.state())


@app.on_event("startup")
async def _startup() -> None:
    if settings["program_on"]:
        hub.start_program()
    app.state.ticker = asyncio.create_task(_ticker())


@app.on_event("shutdown")
async def _shutdown() -> None:
    ledger.save(force=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="TikTok canlı yayın bağış animasyonları")
    parser.add_argument("--user", default="", help="TikTok kullanıcı adı (yayın açıkken bağlanır)")
    parser.add_argument("--mode", default=MODES[0], choices=MODES, help="Başlangıç animasyon modu")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    hub.mode = args.mode

    if args.user:

        @app.on_event("startup")
        async def _autoconnect() -> None:
            await bridge.start(args.user)

    print(f"\n  Kontrol paneli : http://{args.host}:{args.port}/")
    print(f"  Overlay (OBS)  : http://{args.host}:{args.port}/overlay\n")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
