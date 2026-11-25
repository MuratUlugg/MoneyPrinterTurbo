import asyncio
import unittest
from types import SimpleNamespace

from live_overlay import server


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
        self.bridge = server.TikTokBridge()

    def tearDown(self):
        server.hub.broadcast = self._original

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
        self.assertEqual(self.sent[0]["user"], {"id": "ayse", "name": "Ayşe", "avatar": ""})


if __name__ == "__main__":
    unittest.main()
