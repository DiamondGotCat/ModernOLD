import sys

class ModernLogging:
    def __init__(self, process_name):
        self.process_name = process_name

    def log(self, message, level="INFO"):
        if level == "INFO":
            print(self._make(message, level="INFO", color=34))
        elif level == "WARNING":
            print(self._make(message, level="WARNING", color=33))
        elif level == "ERROR":
            print(self._make(message, level="ERROR", color=31))
        else:
            print(self._make(message, level=level, color=35))

    def _make(self, message, level="INFO", color=34):
        return f"{self.process_name} - {self._color(color)}{level}{self._color(0)} - {message}"

    def _color(self, color_code):
        return f"\033[{color_code}m"