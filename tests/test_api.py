import os
import socket
import subprocess
import sys
import time
import urllib.request
import unittest


def get_free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class CityFactsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.port = get_free_port()

        env = os.environ.copy()
        env["PORT"] = str(cls.port)

        cls.process = subprocess.Popen(
            [sys.executable, "app.py"],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for _ in range(50):
            if cls.process.poll() is not None:
                raise RuntimeError("Server failed to start")

            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{cls.port}/healthz",
                    timeout=1
                )
                return
            except Exception:
                time.sleep(0.1)

        raise RuntimeError("Server did not start")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait()

    def get(self, path):
        url = f"http://127.0.0.1:{self.port}{path}"

        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status, response.read().decode()

    def test_root(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("City Facts API", body)

    def test_health(self):
        status, body = self.get("/healthz")
        self.assertEqual(status, 200)
        self.assertIn("ok", body)

    def test_city(self):
        status, body = self.get("/city/almaty")
        self.assertEqual(status, 200)
        self.assertIn("Almaty", body)


if __name__ == "__main__":
    unittest.main()