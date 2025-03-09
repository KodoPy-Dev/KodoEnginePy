
import time
import inspect


class FCOLS:
    BLACK   = "\033[30m"
    WHITE   = "\033[37m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    BLUE    = "\033[34m"
    YELLOW  = "\033[33m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"


class FMODS:
    RESET     = "\033[0m"
    BOLD      = "\033[1m"
    UNDERLINE = "\033[4m"


def debug_print(msg=""):
    stack = inspect.stack()
    caller_frame = stack[1]
    module = inspect.getmodule(caller_frame[0])
    module_name = module.__name__ if module else "<unknown>"
    function_name = caller_frame.function
    line_number = caller_frame.lineno
    traced = []
    for frame in stack[1:]:
        mod = inspect.getmodule(frame[0])
        mod_name = mod.__name__ if mod else "<unknown>"
        traced.append(f"{mod_name}.{frame.function}")
    print(f"{FCOLS.RED}{'-' * 120}", FMODS.RESET)
    print(f"• {time.ctime()}")
    for i, trace in enumerate(reversed(traced)):
        print(f"{i+1}) {trace}")
    print(f"• {FCOLS.GREEN}{function_name}{FMODS.RESET} • {FCOLS.CYAN}{line_number}{FMODS.RESET}")
    print(f"• {FMODS.BOLD}{msg}{FMODS.RESET}")
    print(f"{FCOLS.RED}{'-' * 120}{FMODS.RESET}")
    print(FMODS.RESET)