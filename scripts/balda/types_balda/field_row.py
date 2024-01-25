from typing import List


class FieldRow:
    def __init__(self, chars: List[str]):
        self.chars = chars

    def __str__(self) -> str:
        return str(self.chars)
