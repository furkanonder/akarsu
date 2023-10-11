import re
import sys
import types
from typing import Any, Final, cast

TOOL: Final[int] = 2
PY_CALLABLES: Final[tuple] = (types.FunctionType, types.MethodType)
MONITOR = sys.monitoring  # type:ignore

EVENTS = MONITOR.events
TRACKED_EVENTS: Final[tuple[tuple[int, str], ...]] = (
    (EVENTS.PY_START, "PY_START"),
    (EVENTS.PY_RESUME, "RESUME"),
    (EVENTS.PY_THROW, "THROW"),
    (EVENTS.PY_RETURN, "PY_RETURN"),
    (EVENTS.PY_YIELD, "YIELD"),
    (EVENTS.PY_UNWIND, "UNWIND"),
    (EVENTS.C_RAISE, "C_RAISE"),
    (EVENTS.C_RETURN, "C_RETURN"),
    (EVENTS.EXCEPTION_HANDLED, "EXCEPTION_HANDLED"),
    (EVENTS.STOP_ITERATION, "STOP ITERATION"),
)
EVENT_SET: Final[int] = EVENTS.CALL + sum(ev for ev, _ in TRACKED_EVENTS)
PATTERN: Final[str] = r" at 0x[0-9a-f]+"


class Akarsu:
    def __init__(self, code: str, file_name: str) -> None:
        self.code = code
        self.file_name = file_name

    def format_func_name(self, event: tuple[str, str, str]) -> tuple[str, str, str]:
        event_type, file_name, func_name = event
        return (event_type, file_name, re.sub(PATTERN, "", func_name))

    def profile(self) -> list[tuple[str, str, str]]:
        events = []

        if code := self.code.strip():
            indented_code = "\n".join(f"\t{line}" for line in code.splitlines())
            source = f"def ____wrapper____():\n{indented_code}\n____wrapper____()"
            code = compile(source, self.file_name, "exec")  # type:ignore

            for event, event_name in TRACKED_EVENTS:

                def record(
                    *args: tuple[types.CodeType, int], event_name: str = event_name
                ) -> None:
                    code = cast(types.CodeType, args[0])
                    events.append((event_name, code.co_filename, code.co_name))

                MONITOR.register_callback(TOOL, event, record)

            def record_call(
                code: types.CodeType, offset: int, obj: Any, arg: Any
            ) -> None:
                file_name = code.co_filename
                if isinstance(obj, PY_CALLABLES):
                    events.append(("PY_CALL", file_name, obj.__code__.co_name))
                else:
                    events.append(("C_CALL", file_name, str(obj)))

            MONITOR.use_tool_id(TOOL, "Akarsu")
            MONITOR.register_callback(TOOL, EVENTS.CALL, record_call)
            MONITOR.set_events(TOOL, EVENT_SET)
            try:
                exec(code)
            except:
                pass
            MONITOR.set_events(TOOL, 0)
            MONITOR.free_tool_id(TOOL)

            events = [
                self.format_func_name(event)
                for event in events[2:-3]
                if "____wrapper____" not in event[2]
            ]

        return events
