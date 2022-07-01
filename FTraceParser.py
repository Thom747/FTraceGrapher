from pathlib import Path
from typing import Dict, List

from EventLine import EventLine
from Process import Process


class FTraceParser:

    def __init__(self, input_file_path: Path):
        self.path: Path = input_file_path
        self.processes: Dict[str, Process] = {}
        self.line_number: int = 0
        self.included_prefixes = []

    def parse(self) -> List[Process]:
        with open(self.path, 'r') as file:
            for line in file:
                self.line_number += 1
                line = line.strip('\n')
                self._parse_one(line)
        return list(self.processes.values())

    def include_processes_with_prefix(self, prefix: str):
        self.included_prefixes.append(prefix.lower())

    def _parse_one(self, line: str) -> None:
        if line.lower().startswith("cpu"):
            self._skip_with_reason(line, f"starts with \"{line[0:3]}\"")
            return

        if len(self.included_prefixes) > 0:
            valid_prefix = False
            for prefix in self.included_prefixes:
                if line.strip().lower().startswith(prefix):
                    valid_prefix = True
                    break
            if not valid_prefix:
                self._skip_with_reason(line, f"does not start with whitelisted prefix")
                return

        event_line: EventLine = EventLine(line)
        # print(f"{event_line}")

        try:
            process: Process = self.processes[event_line.process_name]
        except KeyError:
            process: Process = Process(event_line.process_name)
            self.processes[event_line.process_name] = process

        if event_line.event_name == 'funcgraph_exit':
            process.end_function_call()
        elif event_line.event_name == 'funcgraph_entry':
            process.start_function_call(event_line.function_name)
        else:
            self._skip_with_reason(line, f"Unknown event: {event_line.event_name}")

    def _skip_with_reason(self, line: str, reason: str):
        print(f"Skipping line #{self.line_number} \"{line}\".\n  Reason: {reason}")
