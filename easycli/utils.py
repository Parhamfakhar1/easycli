import sys
from typing import List, Dict, Tuple

def parse_args(args: List[str]) -> Tuple[List[str], Dict[str, Any]]:
    """پردازش آرگومان‌ها و پرچم‌ها"""
    positional = []
    flags = {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--"):
            key = arg[2:]
            if i + 1 < len(args) and not args[i+1].startswith("-"):
                flags[key] = args[i+1]
                i += 1
            else:
                flags[key] = True  # برای پرچم‌های bool
        elif arg.startswith("-"):
            key = arg[1:]
            if i + 1 < len(args) and not args[i+1].startswith("-"):
                flags[key] = args[i+1]
                i += 1
            else:
                flags[key] = True
        else:
            positional.append(arg)
        i += 1
    return positional, flags