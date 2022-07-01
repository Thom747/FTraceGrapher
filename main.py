#! ./venv/bin/python3
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List

from FTraceParser import FTraceParser
from Grapher import Grapher
from Process import Process


def main():
    argparser: ArgumentParser = ArgumentParser(description="Python-based visualizer for FTrace function_graph output.")
    argparser.add_argument("path", nargs=1, help="Path to text file created by trace-cmd report")
    argparser.add_argument("prefixes", nargs='*',
                           help="Prefixes of processes to include in graph. Not case-sensitive. Leave empty for all.")
    args: Namespace = argparser.parse_args()
    path_str: str = args.path[0]
    path: Path = Path(path_str)
    prefixes: List[str] = args.prefixes

    ftrace_parser: FTraceParser = FTraceParser(path)
    for prefix in prefixes:
        ftrace_parser.include_processes_with_prefix(prefix)
    processes: List[Process] = ftrace_parser.parse()
    print([proc.current_depth for proc in processes])
    sys.setrecursionlimit(1100)
    grapher: Grapher = Grapher()
    grapher.add_processes(processes)
    grapher.draw()


if __name__ == '__main__':
    main()
