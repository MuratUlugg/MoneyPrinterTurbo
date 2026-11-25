"""Kalıcı veri: yayın defteri (kim ne gönderdi), ayarlar ve ad denetimi.

Overlay tarayıcıda çalışır ve yenilenince belleği silinir; bu yüzden hediyelerin
asıl kaydı burada, sunucuda tutulur ve diske yazılır. Overlay yeniden açıldığında
sıralama, seviyeler ve yayın hedefi buradan geri yüklenir.
"""

from __future__ import annotations

import csv
import io
import json
import re
import time
from pathlib import Path
from typing import Any, Optional

DATA_DIR = Path(__file__).parent / "data"

# ---------------------------------------------------------------------------
# Ayarlar
# ---------------------------------------------------------------------------

# anahtar: (varsayılan, en az, en çok)
NUMERIC = {
    "goal": (300, 10, 1_000_000),       # at yarışı finişi
    "halay": (400, 10, 1_000_000),      # halay coşkusu
    "taki": (500, 10, 1_000_000),       # ilk düğünün takı hedefi
    "tug": (300, 10, 1_000_000),        # halat farkı
    "karpuzMin": (120, 5, 1_000_000),
    "karpuzMax": (450, 10, 1_000_000),
    "bahsis": (30, 1, 1_000_000),       # davulcuya bahşiş
    "orta": (100, 1, 1_000_000),        # ortaya çıkma
    "buyuk": (100, 1, 1_000_000),       # büyük hediye gösterisi
    "hedef": (2000, 10, 100_000_000),   # yayın hedefi
    "konuk": (6, 0, 16),                # hazır oturan adsız konuk
    "anonsMin": (10, 1, 1_000_000),     # sesli anons için en az jeton
}
DEFAULT_PROGRAM = [{"mode": "halay", "min": 10}, {"mode": "taki", "min": 6}, {"mode": "race", "min": 5}]


def default_settings() -> dict[str, Any]:
    s: dict[str, Any] = {k: v[0] for k, v in NUMERIC.items()}
    s.update(
        cift="",            # sahnedeki pankart
        ses=False,          # davul, altın, alkış sesi
        anons=False,        # hediyeleri sesli oku
        kalite="oto",       # oto | yuksek | dusuk
        yasak=[],           # adlarda geçmesi yasak kelimeler
        gizli=[],           # adı gizlenecek kullanıcı kimlikleri
        program_on=False,   # modları sırayla kendiliğinden değiştir
        program=[dict(p) for p in DEFAULT_PROGRAM],
    )
    return s


def clean_settings(raw: dict[str, Any], modes: tuple[str, ...], base: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """Dışarıdan gelen ayarları doğrular; bilinmeyen ya da bozuk alanları yok sayar."""
    s = dict(base or default_settings())
    for key, (_default, low, high) in NUMERIC.items():
        if key in raw:
            try:
                s[key] = max(low, min(high, int(float(raw[key]))))
            except (TypeError, ValueError):
                pass
    if s["karpuzMax"] <= s["karpuzMin"]:
        s["karpuzMax"] = s["karpuzMin"] + 10
    if "cift" in raw:
        s["cift"] = str(raw["cift"] or "").strip()[:28]
    for key in ("ses", "anons", "program_on"):
        if key in raw:
            s[key] = bool(raw[key])
    if raw.get("kalite") in ("oto", "yuksek", "dusuk"):
        s["kalite"] = raw["kalite"]
    for key in ("yasak", "gizli"):
        if key in raw:
            items = raw[key] if isinstance(raw[key], list) else re.split(r"[,\n]", str(raw[key] or ""))
            s[key] = [str(i).strip()[:40] for i in items if str(i).strip()][:200]
    if isinstance(raw.get("program"), list):
        steps = []
        for step in raw["program"][:12]:
            try:
                if step["mode"] in modes:
                    steps.append({"mode": step["mode"], "min": max(1, min(180, int(float(step["min"]))))})
            except (KeyError, TypeError, ValueError):
                continue
        if steps:
            s["program"] = steps
    return s


def _read(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return fallback


def _write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)  # yarım yazılmış dosya kalmasın


# ---------------------------------------------------------------------------
# Ad denetimi: yayına büyük harflerle çıkan adlar için
# ---------------------------------------------------------------------------

# Kısa ve temkinli bir başlangıç listesi; yayıncı panelden kendi kelimelerini ekler.
DEFAULT_BLOCKED = ("amk", "aq", "orospu", "piç", "pic", "sik", "yarrak", "göt", "gavat", "pezevenk", "kahpe", "ibne")
_LINK = re.compile(r"(https?://|www\.|\.com|\.net|\.org|t\.me/|wa\.me/)", re.I)
_PHONE = re.compile(r"(\d[\s.\-]?){9,}")
_TR_LOWER = str.maketrans("IİŞĞÜÖÇ", "ıişğüöç")
_LEET = str.maketrans("013457@$", "oieastas")
SAFE_NAME = "Misafir"


def _norm(text: str) -> str:
    return text.translate(_TR_LOWER).lower()


def clean_name(name: str, extra_blocked: tuple[str, ...] | list[str] = ()) -> str:
    """Adı yayına uygun hale getirir; reklam, telefon ya da yasak kelime varsa 'Misafir' döner."""
    name = re.sub(r"[\x00-\x1f​-‏‪-‮⁦-⁩]", "", str(name or "")).strip()[:24]
    if not name:
        return SAFE_NAME
    if _LINK.search(name) or _PHONE.search(name):
        return SAFE_NAME
    flat = re.sub(r"[^a-zçğıöşü]", "", _norm(name).translate(_LEET))
    words = set(re.split(r"[^a-zçğıöşü0-9]+", _norm(name)))
    for bad in (*DEFAULT_BLOCKED, *extra_blocked):
        bad_n = re.sub(r"[^a-zçğıöşü]", "", _norm(str(bad)))
        if not bad_n:
            continue
        # Kısa kelimeler ("aq", "sik") yalnızca ayrı kelime olarak yakalanır; yoksa "Sıkıntı" gibi masum adlar da gider.
        if (len(bad_n) <= 3 and bad_n in words) or (len(bad_n) > 3 and bad_n in flat):
            return SAFE_NAME
    return name


# ---------------------------------------------------------------------------
# Yayın defteri
# ---------------------------------------------------------------------------


class Ledger:
    """Bir yayının hediye kaydı + yayınlar arası (tüm zamanlar) toplamlar."""

    def __init__(self, data_dir: Path = DATA_DIR) -> None:
        self.dir = data_dir
        self.dirty = False
        self.alltime: dict[str, dict[str, Any]] = _read(self.dir / "alltime.json", {})
        saved = _read(self.dir / "current.json", None)
        self._reset()
        if isinstance(saved, dict) and "users" in saved:
            self.__dict__.update({k: saved[k] for k in self._fields() if k in saved})

    @staticmethod
    def _fields() -> tuple[str, ...]:
        return ("started", "users", "total", "by_mode", "minutes", "counts", "biggest", "catalog")

    def _reset(self) -> None:
        self.started = time.time()
        self.users: dict[str, dict[str, Any]] = {}
        self.total = 0
        self.by_mode: dict[str, int] = {}
        self.minutes: dict[str, int] = {}      # yayının kaçıncı dakikası -> jeton
        self.counts = {"gift": 0, "like": 0, "comment": 0, "follow": 0, "share": 0}
        self.biggest: Optional[dict[str, Any]] = None
        self.catalog: dict[str, dict[str, Any]] = {}  # bu yayında görülen hediyeler

    # -- kayıt --
    def count(self, kind: str, n: int = 1) -> None:
        if kind in self.counts:
            self.counts[kind] += n
            self.dirty = True

    def add_gift(self, user: dict[str, str], gift: dict[str, Any], total: int, mode: str) -> int:
        """Hediyeyi işler; kullanıcının önceki yayınlardaki toplamını döndürür."""
        uid = user["id"]
        u = self.users.setdefault(uid, {"name": user["name"], "avatar": user.get("avatar", ""), "total": 0, "gifts": 0})
        u["name"], u["avatar"] = user["name"], user.get("avatar", "") or u["avatar"]
        u["total"] += total
        u["gifts"] += 1
        self.total += total
        self.by_mode[mode] = self.by_mode.get(mode, 0) + total
        minute = str(int((time.time() - self.started) // 60))
        self.minutes[minute] = self.minutes.get(minute, 0) + total
        self.counts["gift"] += 1
        if not self.biggest or total > self.biggest["amount"]:
            self.biggest = {"name": user["name"], "amount": total, "gift": gift.get("name", "")}
        name = str(gift.get("name", ""))[:40]
        if name:
            self.catalog[name] = {"diamonds": int(gift.get("diamonds", 1)), "image": gift.get("image", "")}
        self.dirty = True
        return int(self.alltime.get(uid, {}).get("total", 0))

    # -- okuma --
    def snapshot(self) -> dict[str, Any]:
        """Overlay açıldığında sıralamayı geri kurması için."""
        top = sorted(self.users.items(), key=lambda kv: -kv[1]["total"])[:300]
        return {
            "type": "restore",
            "total": self.total,
            "users": [{"id": uid, "name": u["name"], "avatar": u["avatar"], "total": u["total"]} for uid, u in top],
            "catalog": sorted(({"name": n, **g} for n, g in self.catalog.items()), key=lambda g: g["diamonds"]),
        }

    def report(self) -> dict[str, Any]:
        users = sorted(self.users.values(), key=lambda u: -u["total"])
        last = max((int(m) for m in self.minutes), default=0)
        alltime = sorted(self.alltime.values(), key=lambda u: -u["total"])[:10]
        return {
            "started": self.started,
            "minutes_live": int((time.time() - self.started) // 60),
            "total": self.total,
            "gifters": len(users),
            "average": round(self.total / len(users), 1) if users else 0,
            "counts": self.counts,
            "by_mode": self.by_mode,
            "biggest": self.biggest,
            "top": [{"name": u["name"], "total": u["total"], "gifts": u["gifts"]} for u in users[:10]],
            "timeline": [self.minutes.get(str(m), 0) for m in range(last + 1)],
            "alltime": [{"name": u["name"], "total": u["total"], "streams": u.get("streams", 1)} for u in alltime],
        }

    def report_csv(self) -> str:
        out = io.StringIO()
        w = csv.writer(out)
        w.writerow(["sira", "ad", "jeton", "hediye_sayisi"])
        for i, u in enumerate(sorted(self.users.values(), key=lambda u: -u["total"]), 1):
            w.writerow([i, u["name"], u["total"], u["gifts"]])
        return out.getvalue()

    # -- yaşam döngüsü --
    def new_stream(self) -> None:
        """Yayını kapatır: toplamları 'tüm zamanlar'a ekler, raporu arşivler, defteri sıfırlar."""
        if self.users:
            for uid, u in self.users.items():
                a = self.alltime.setdefault(uid, {"name": u["name"], "total": 0, "streams": 0})
                a["name"] = u["name"]
                a["total"] += u["total"]
                a["streams"] = a.get("streams", 0) + 1
            _write(self.dir / "alltime.json", self.alltime)
            _write(self.dir / "reports" / (time.strftime("%Y%m%d-%H%M%S", time.localtime(self.started)) + ".json"), self.report())
        self._reset()
        self.save(force=True)

    def save(self, force: bool = False) -> None:
        if self.dirty or force:
            _write(self.dir / "current.json", {k: getattr(self, k) for k in self._fields()})
            self.dirty = False


def load_settings(modes: tuple[str, ...], data_dir: Path = DATA_DIR) -> dict[str, Any]:
    return clean_settings(_read(data_dir / "settings.json", {}), modes)


def save_settings(settings: dict[str, Any], data_dir: Path = DATA_DIR) -> None:
    _write(data_dir / "settings.json", settings)
