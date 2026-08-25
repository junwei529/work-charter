import unittest

from src.worker import worker_enabled, worker_name


class WorkerTests(unittest.TestCase):
    def test_name(self) -> None:
        self.assertEqual(worker_name(), "fixture-worker")

    def test_enabled(self) -> None:
        self.assertTrue(worker_enabled())


if __name__ == "__main__":
    unittest.main()
