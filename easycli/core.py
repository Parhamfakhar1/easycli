import sys
from typing import Callable, Any

class CLI:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.commands = {}  # ذخیره دستورات

    def command(self, name: str, description: str = ""):
        """دکوراتور برای ثبت دستورات"""
        def decorator(func: Callable) -> Callable:
            self.commands[name] = {
                "func": func,
                "description": description
            }
            return func
        return decorator

    def run(self):
        """پردازش آرگومان‌های خط فرمان و اجرای دستور"""
        args = sys.argv[1:]  # آرگومان‌ها بدون نام اسکریپت
        if not args:
            self._show_help()
            return

        command_name = args[0]
        command_args = args[1:]

        if command_name not in self.commands:
            print(f"Error: Command '{command_name}' not found")
            self._show_help()
            return

        # اجرای تابع دستور با آرگومان‌ها
        command = self.commands[command_name]
        try:
            command["func"](*command_args)
        except TypeError as e:
            print(f"Error: Invalid arguments for '{command_name}': {e}")
            self._show_help(command_name)

    def _show_help(self, command_name: str = None):
        """نمایش راهنما"""
        if command_name and command_name in self.commands:
            cmd = self.commands[command_name]
            print(f"{command_name}: {cmd['description']}")
        else:
            print(f"{self.name}: {self.description}")
            print("Available commands:")
            for name, cmd in self.commands.items():
                print(f"  {name}: {cmd['description']}")