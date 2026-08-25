import unittest

from src.range_utils import inclusive_count


class InclusiveCountTests(unittest.TestCase):
    def test_counts_both_endpoints(self) -> None:
        self.assertEqual(inclusive_count(4, 6), 3)

    def test_empty_when_end_precedes_start(self) -> None:
        self.assertEqual(inclusive_count(6, 4), 0)


if __name__ == "__main__":
    unittest.main()
