def partition_batches(values: list[int], batch_size: int) -> list[list[int]]:
    return [
        values[index : index + batch_size]
        for index in range(0, len(values) - batch_size + 1, batch_size)
    ]
