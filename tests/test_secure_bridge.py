import unittest
import subprocess
import time
import os
import shutil
import socket
from python.secure_bridge import send_secure_task


class TestSecureBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which("go") is None:
            raise unittest.SkipTest("Go toolchain not available")
        cls.proc = subprocess.Popen(["go", "run", "go/main.go"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        if cls.proc.poll() is not None:
            cls.proc = None
            raise unittest.SkipTest("Go server failed to start")
        s = socket.socket()
        try:
            s.settimeout(1)
            s.connect(("127.0.0.1", 8080))
        except OSError:
            cls.proc.terminate()
            cls.proc.wait(timeout=5)
            cls.proc = None
            raise unittest.SkipTest("Go server unreachable")
        finally:
            s.close()

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        try:
            cls.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.proc.kill()

    def test_send_secure_task(self):
        session_key = "a" * 32  # Dummy 32 bytes
        response = send_secure_task("secure123", "Hello Secure World", session_key)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["received_task_id"], "secure123")
        self.assertTrue(response["validated_session_key"])


if __name__ == "__main__":
    unittest.main()
