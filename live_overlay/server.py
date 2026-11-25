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
import json
import time
from pathlib import Path
from typing import Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

STATIC_DIR = Path(__file__).parent / "static"
MODES = ("halay", "race", "taki", "tug", "karpuz")
HTML_PREFIX = '<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><script>window.LIVE_SERVER=1</script>'


class Hub:
    """Bağlı overlay/panel istemcilerini ve ortak durumu tutar."""

    def __init__(self) -> None:
        self.clients: set[WebSocket] = set()
        self.mode: str = MODES[0]
        self.tiktok_user: str = ""
        self.tiktok_status: str = "disconnected"  # disconnected | connecting | connected | error
        self.tiktok_error: str = ""

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
        }

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
                await hub.broadcast(
                    {"type": "like", "user": _user(event.user), "count": max(1, int(getattr(event, "count", 1) or 1))}
                )

            @client.on(FollowEvent)
            async def _on_follow(event: Any) -> None:
                await hub.broadcast({"type": "follow", "user": _user(event.user)})

            @client.on(ShareEvent)
            async def _on_share(event: Any) -> None:
                await hub.broadcast({"type": "share", "user": _user(event.user)})

            @client.on(CommentEvent)
            async def _on_comment(event: Any) -> None:
                await hub.broadcast(
                    {"type": "comment", "user": _user(event.user), "text": str(getattr(event, "comment", "") or "")[:200]}
                )

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
        await hub.broadcast(
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


def _page(name: str) -> HTMLResponse:
    # Sayfalar gövde parçası olarak saklanır; doctype burada eklenir.
    body = (STATIC_DIR / name).read_text(encoding="utf-8")
    return HTMLResponse(HTML_PREFIX + body, headers={"Cache-Control": "no-store"})


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
    await hub.broadcast(hub.state())
    return hub.state()


@app.post("/api/reset")
async def reset() -> dict[str, bool]:
    await hub.broadcast({"type": "reset"})
    return {"ok": True}


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
    user = {"id": "sim:" + body.name.lower(), "name": body.name, "avatar": ""}
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
    await hub.broadcast(event)
    return {"ok": True}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    hub.clients.add(ws)
    try:
        await ws.send_text(json.dumps(hub.state(), ensure_ascii=False))
        while True:
            await ws.receive_text()  # istemciden veri beklenmez; bağlantıyı açık tutar
    except WebSocketDisconnect:
        pass
    finally:
        hub.clients.discard(ws)


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
