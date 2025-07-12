import unittest
import subprocess
import time
import os
from python.secure_bridge import send_secure_task


class TestSecureBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Go server
        cls.proc = subprocess.Popen(["go", "run", "go/main.go"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Give the server a moment to start and compile
        time.sleep(2)

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
