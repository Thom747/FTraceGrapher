from typing import Optional, List, Union


class EventLine:
    def __init__(self, input_str: str):
        [self.process_name, self.cpu, self.timestamp, self.event_name] = _parse_line_head(input_str)
        self.function_name: Optional[str] = _get_function(input_str)

    def __str__(self):
        return self.__dict__.__str__()

def _get_function(input_str: str) -> Optional[str]:
    function: str = input_str.strip()
    function = function.split("|")[1]
    if function.strip() == '}':
        return None
    function = function.strip("{").strip()
    return function


def _parse_line_head(input_str: str) -> List[Union[str, int, float]]:
    strs: List[str] = input_str.strip().split()[0:4]
    values = [strs[0],
              int(strs[1].strip('[]')),
              float(strs[2].strip(':')),
              strs[3].strip(':')
              ]
    return values
