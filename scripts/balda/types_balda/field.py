from typing import List
from .field_row import FieldRow


class Field:
    def __init__(self, rows: List[FieldRow]):
        self.rows = rows

    @property
    def size(self) -> int:
        return len(self.rows)

    def __str__(self) -> str:
        return str(self.rows)
