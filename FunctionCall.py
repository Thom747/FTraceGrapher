from typing import Optional, List


class FunctionCall:
    def __init__(self, name: str, parent: Optional['FunctionCall']):
        self.name = name
        self.parent: Optional[FunctionCall] = parent
        self.children: List[FunctionCall] = []
        if self.parent is not None:
            self.parent.add_child(self)
            self.depth = self.parent.depth + 1
        else:
            self.depth = 1

    def add_child(self, child: 'FunctionCall'):
        self.children.append(child)

    def __str__(self):
        return f"{self.name} d:{self.depth}"
