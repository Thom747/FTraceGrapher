from typing import Optional, List

from FunctionCall import FunctionCall


class Process:
    def __init__(self, name: str):
        self.name: str = name
        self.children: List[FunctionCall] = []
        self.active_function_call: Optional[FunctionCall] = None
        self.current_depth: int = 0
        self.depth = 0

    def __str__(self):
        return self.name

    def start_function_call(self, name: str):
        child_fc: FunctionCall = FunctionCall(name, self.active_function_call)
        self.active_function_call = child_fc
        if self.active_function_call.parent is None:
            self.children.append(self.active_function_call)
        self.current_depth += 1

    def end_function_call(self):
        try:
            print(f"{self.name}: End call {self.active_function_call.name}, depth={self.current_depth}")
            self.active_function_call = self.active_function_call.parent

            self.current_depth -= 1
        except AttributeError:
            print(
                "Warning: log shows an unmatched end of function, likely due to dropped events. Output past this "
                "point can be unreliable.")
