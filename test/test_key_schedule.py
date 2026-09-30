"""Key schedule tests. Run from the project root:  python -m unittest tests.test_key_schedule -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import crypto_engine  # noqa: E402

KEY = "133457799BBCDFF1"  # standard DES test key


class KeyScheduleMath(unittest.TestCase):
    def setUp(self):
        self.r = crypto_engine.get_key_schedule(KEY)

    def test_stages(self):
        r = self.r
        self.assertEqual(r["original_64"], format(int(KEY, 16), "064b"))
        self.assertEqual(r["pc_1"], "11110000110011001010101011110101010101100110011110001111")
        self.assertEqual(r["c0_d0"]["c0"], "1111000011001100101010101111")
        self.assertEqual(r["c0_d0"]["d0"], "0101010101100110011110001111")
        self.assertEqual(r["shifts"], [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1])

    def test_published_round_keys(self):
        self.assertEqual(self.r["round_keys_hex"][0], "1B02EFFC7072")   # K1
        self.assertEqual(self.r["round_keys_hex"][15], "CB3D8B0E17F5")  # K16

    def test_shapes(self):
        r = self.r
        self.assertEqual(len(r["c"]), 17)
        self.assertEqual(len(r["d"]), 17)
        self.assertEqual(len(r["round_keys"]), 16)
        self.assertTrue(all(len(k) == 48 and set(k) <= {"0", "1"} for k in r["round_keys"]))
        self.assertEqual(r["c"][16], r["c"][0])  # 28 total shifts = full rotation
        self.assertEqual(r["d"][16], r["d"][0])

    def test_lowercase_key(self):
        self.assertEqual(crypto_engine.get_key_schedule(KEY.lower()), self.r)


class KeyScheduleApi(unittest.TestCase):
    def setUp(self):
        from app import app
        self.client = app.test_client()

    def test_ok(self):
        res = self.client.post("/api/key-schedule", json={"key": KEY})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["round_keys_hex"][0], "1B02EFFC7072")

    def test_bad_keys(self):
        for bad in ["", "1234", "ZZZZ57799BBCDFF1", KEY + "00"]:
            res = self.client.post("/api/key-schedule", json={"key": bad})
            self.assertEqual(res.status_code, 400, bad)
            self.assertIn("error", res.get_json())


if __name__ == "__main__":
    unittest.main()
