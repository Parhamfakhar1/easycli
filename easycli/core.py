import sys
import inspect
from typing import Callable, Any, Dict
from .utils import parse_args  # از utils.py

class CommandGroup:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.subgroups: Dict[str, 'CommandGroup'] = {}

    def command(self, name: str, description: str = ""):
        def decorator(func: Callable) -> Callable:
            self.commands[name] = {
                "func": func,
                "description": description,
                "signature": inspect.signature(func)
            }
            return func
        return decorator

    def group(self, name: str, description: str = ""):
        subgroup = CommandGroup(name, description)
        self.subgroups[name] = subgroup
        return subgroup

class CLI:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.root = CommandGroup("root")

    def command(self, name: str, description: str = ""):
        return self.root.command(name, description)

    def group(self, name: str, description: str = ""):
        return self.root.group(name, description)

    def run(self):
        args = sys.argv[1:]
        if not args or args[0] in ["--help", "-h"]:
            self._show_help(self.root)
            return

        current_group = self.root
        command_name = None
        command_args = args[:]
        path = []

        # پیدا کردن دستور یا گروه زیرمجموعه
        while command_args:
            part = command_args[0]
            if part in current_group.subgroups:
                current_group = current_group.subgroups[part]
                path.append(part)
                command_args = command_args[1:]
            elif part in current_group.commands:
                command_name = part
                command_args = command_args[1:]
                break
            else:
                print(f"Error: Invalid command or group '{part}'")
                self._show_help(current_group)
                return

        if command_name is None:
            print("Error: No command specified")
            self._show_help(current_group)
            return

        command = current_group.commands[command_name]

        # پردازش آرگومان‌ها و پرچم‌ها
        try:
            positional_args, flags = parse_args(command_args)
            sig = command["signature"]
            bound_args = sig.bind(*positional_args, **flags)
            command["func"](*bound_args.args, **bound_args.kwargs)
        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
            self._show_help(current_group, command_name)

    def _show_help(self, group: CommandGroup, command_name: str = None):
        path = " ".join(path for path in group.name.split() if path != "root") if group.name != "root" else ""
        if command_name and command_name in group.commands:
            cmd = group.commands[command_name]
            print(f"Usage: {self.name} {path} {command_name} [args] [flags]")
            print(f"{command_name}: {cmd['description']}")
            print("Arguments:")
            for param in cmd["signature"].parameters.values():
                print(f"  {param.name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'Any'}")
        else:
            print(f"Usage: {self.name} [command] [subcommand] ... [args] [flags]")
            print(f"{self.description}")
            if group.commands:
                print("Commands:")
                for name, cmd in group.commands.items():
                    print(f"  {name}: {cmd['description']}")
            if group.subgroups:
                print("Groups:")
                for name, sub in group.subgroups.items():
                    print(f"  {name}: {sub.description}")