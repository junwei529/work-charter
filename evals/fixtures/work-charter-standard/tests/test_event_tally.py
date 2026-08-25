import unittest

from src.event_tally import count_by_kind


class EventTallyTests(unittest.TestCase):
    def test_empty_input(self) -> None:
        self.assertEqual(count_by_kind([]), {})


if __name__ == "__main__":
    unittest.main()
