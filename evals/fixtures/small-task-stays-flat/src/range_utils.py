def inclusive_count(start: int, end: int) -> int:
    if end < start:
        return 0
    return end - start
