import sys

class ModernProgressBar:
    _active_bars = []
    _last_rendered = False

    def __init__(self, total, process_name, process_color):
        self.total = total
        self.current = 0
        self.process_name = process_name
        self.process_color = process_color
        self.index = len(ModernProgressBar._active_bars)
        ModernProgressBar._active_bars.append(self)
        self._initial_render()

    def _initial_render(self):
        print()  # Reserve a line for the progress bar

    def start(self):
        self._render()

    def update(self, amount=1):
        self.current += amount
        if self.current > self.total:
            self.current = self.total
        self._render()

    def finish(self):
        self.current = self.total
        self._render(final=True)

    def _render(self, final=False):
        progress = self.current / self.total
        bar = self._progress_bar(progress)
        percentage = f"{progress:.2%}"
        status = "[DONE]" if final else f"[{self.current}/{self.total}]"
        line = f"{self.process_name} - ({self._color(self.process_color)}{bar}{self._color(0)}) {percentage} {status}"
        
        # Move cursor to the progress bar line
        sys.stdout.write(f"\033[{len(ModernProgressBar._active_bars) - self.index}A")  # Move up
        sys.stdout.write("\033[K")  # Clear the line
        print(line)
        # Move cursor back to the bottom
        sys.stdout.write(f"\033[{len(ModernProgressBar._active_bars) - self.index}B")
        sys.stdout.flush()

    def _progress_bar(self, progress):
        bar_length = 20
        empty_bar = "/"
        filled_bar = "-"
        filled_length = int(progress * bar_length)
        return f"{filled_bar * filled_length}{empty_bar * (bar_length - filled_length)}"

    def _color(self, color_code):
        return f"\033[{color_code}m"