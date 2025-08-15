from typing import List


class PaginationDTO:
    def __init__(self, items: List, limit: int, offset: int, total: int):
        self.items = items
        self.limit = limit
        self.offset = offset
        self.total = total


