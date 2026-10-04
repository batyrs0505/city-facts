import os
import socket
import subprocess
import sys
import time
import urllib.request


def get_free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_for_server(port, process):
    url = f"http://127.0.0.1:{port}/healthz"

    for _ in range(50):
        if process.poll() is not None:
            return False

        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.1)

    return False


def get(path, port):
    url = f"http://127.0.0.1:{port}{path}"

    with urllib.request.urlopen(url, timeout=2) as response:
        return response.status, response.read().decode()


port = get_free_port()

env = os.environ.copy()
env["PORT"] = str(port)

process = subprocess.Popen(
    [sys.executable, "app.py"],
    env=env,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

passed = 0
total = 3

try:
    if not wait_for_server(port, process):
        print(f"TESTS: 0/{total}")
        sys.exit(1)

    # Test 1: root endpoint
    status, body = get("/", port)
    assert status == 200
    assert "City Facts API" in body
    passed += 1

    # Test 2: health endpoint
    status, body = get("/healthz", port)
    assert status == 200
    assert "ok" in body
    passed += 1

    # Test 3: city endpoint
    status, body = get("/city/almaty", port)
    assert status == 200
    assert "Almaty" in body
    assert "Kazakhstan" in body
    passed += 1

    print(f"TESTS: {passed}/{total}")

except Exception as e:
    print(f"TESTS: {passed}/{total}")
    print(f"Test failed: {e}")
    sys.exit(1)

finally:
    process.terminate()
    process.wait()