import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from live_overlay import server, store


def _gift_event(repeat_count, repeat_end=0, streakable=True, diamonds=5):
    return SimpleNamespace(
        user=SimpleNamespace(unique_id="ayse", nickname="Ayşe", avatar_thumb=None),
        gift=SimpleNamespace(name="Gül", diamond_count=diamonds, streakable=streakable, id=1, image=None, icon=None),
        gift_id=1,
        group_id=42,
        repeat_count=repeat_count,
        repeat_end=repeat_end,
    )


class TestGiftStreaks(unittest.TestCase):
    def setUp(self):
        self.sent = []

        async def fake_broadcast(message):
            self.sent.append(message)

        self._original = server.hub.broadcast
        server.hub.broadcast = fake_broadcast
        self._ledger = server.ledger  # testler gerçek yayın defterine yazmasın
        self._tmp = tempfile.TemporaryDirectory()
        server.ledger = store.Ledger(Path(self._tmp.name))
        self.bridge = server.TikTokBridge()

    def tearDown(self):
        server.hub.broadcast = self._original
        server.ledger = self._ledger
        self._tmp.cleanup()

    def _send(self, *events):
        async def run():
            for event in events:
                await self.bridge._handle_gift(event)

        asyncio.run(run())

    def test_streak_emits_only_the_difference(self):
        # TikTok seri hediyede artan toplamı tekrar tekrar gönderir: 1, 3, 3(bitiş).
        self._send(_gift_event(1), _gift_event(3), _gift_event(3, repeat_end=1))
        self.assertEqual([m["gift"]["count"] for m in self.sent], [1, 2])
        self.assertEqual(sum(m["total"] for m in self.sent), 15)

    def test_new_streak_after_end_counts_from_zero(self):
        self._send(_gift_event(2, repeat_end=1), _gift_event(1))
        self.assertEqual([m["gift"]["count"] for m in self.sent], [2, 1])

    def test_non_streakable_gift_uses_full_count(self):
        self._send(_gift_event(1, streakable=False, diamonds=100))
        self.assertEqual(self.sent[0]["total"], 100)
        user = self.sent[0]["user"]
        self.assertEqual((user["id"], user["name"], user["avatar"]), ("ayse", "Ayşe", ""))


class TestLedger(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _gift(self, ledger, uid, total, mode="halay"):
        return ledger.add_gift({"id": uid, "name": uid.title(), "avatar": ""}, {"name": "Gül", "diamonds": 1, "image": ""}, total, mode)

    def test_totals_survive_a_restart(self):
        ledger = store.Ledger(self.dir)
        self._gift(ledger, "ayse", 30)
        self._gift(ledger, "mehmet", 100, mode="taki")
        self._gift(ledger, "ayse", 5)
        ledger.save()
        restored = store.Ledger(self.dir).snapshot()  # sunucu yeniden açıldı
        self.assertEqual(restored["total"], 135)
        self.assertEqual([(u["id"], u["total"]) for u in restored["users"]], [("mehmet", 100), ("ayse", 35)])

    def test_new_stream_moves_totals_to_alltime(self):
        ledger = store.Ledger(self.dir)
        self.assertEqual(self._gift(ledger, "ayse", 40), 0)
        ledger.new_stream()
        self.assertEqual(ledger.snapshot()["users"], [])
        self.assertEqual(self._gift(ledger, "ayse", 1), 40)  # geri gelen bağışçı tanınır
        self.assertTrue(list((self.dir / "reports").glob("*.json")))

    def test_report_breaks_down_by_mode(self):
        ledger = store.Ledger(self.dir)
        self._gift(ledger, "ayse", 30)
        self._gift(ledger, "can", 70, mode="race")
        report = ledger.report()
        self.assertEqual(report["by_mode"], {"halay": 30, "race": 70})
        self.assertEqual((report["gifters"], report["average"], report["biggest"]["amount"]), (2, 50.0, 70))


class TestNamesAndSettings(unittest.TestCase):
    def test_clean_name_blocks_ads_and_profanity_but_not_innocent_names(self):
        self.assertEqual(store.clean_name("Ayşe Yılmaz"), "Ayşe Yılmaz")
        self.assertEqual(store.clean_name("Sıkıntı Yok"), "Sıkıntı Yok")
        self.assertEqual(store.clean_name("takipci.com"), store.SAFE_NAME)
        self.assertEqual(store.clean_name("ara 0532 123 45 67"), store.SAFE_NAME)
        self.assertEqual(store.clean_name("P3Z3V3NK"), store.SAFE_NAME)
        self.assertEqual(store.clean_name("Bahis Kralı", ["bahis"]), store.SAFE_NAME)
        self.assertEqual(store.clean_name(""), store.SAFE_NAME)

    def test_settings_are_clamped_and_unknown_keys_ignored(self):
        s = store.clean_settings({"hedef": "abc", "orta": -5, "konuk": 99, "kalite": "x", "hack": 1, "program": [{"mode": "yok", "min": 3}, {"mode": "taki", "min": 999}]}, server.MODES)
        self.assertEqual((s["hedef"], s["orta"], s["konuk"], s["kalite"]), (2000, 1, 16, "oto"))
        self.assertNotIn("hack", s)
        self.assertEqual(s["program"], [{"mode": "taki", "min": 180}])


if __name__ == "__main__":
    unittest.main()
