import unittest

from src.batches import partition_batches


class PartitionBatchesTests(unittest.TestCase):
    def test_complete_batches(self) -> None:
        self.assertEqual(
            partition_batches([1, 2, 3, 4], 2),
            [[1, 2], [3, 4]],
        )

    def test_empty_input(self) -> None:
        self.assertEqual(partition_batches([], 2), [])

    def test_keeps_final_partial_batch(self) -> None:
        self.assertEqual(
            partition_batches([1, 2, 3], 2),
            [[1, 2], [3]],
        )


if __name__ == "__main__":
    unittest.main()
