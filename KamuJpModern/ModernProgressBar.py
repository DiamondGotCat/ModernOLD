import sys
import threading
import time

class ModernProgressBar:
    _active_bars = []
    _last_rendered = False
    _lock = threading.Lock()

    def __init__(self, total, process_name, process_color, isbusy=True):
        self.total = total
        self.isbusy = isbusy
        self.current = 0
        self.process_name = process_name.strip()
        self.process_color = process_color
        self.index = len(ModernProgressBar._active_bars)
        ModernProgressBar._active_bars.append(self)
        self.log_lines = 0
        self.step = 0
        self.busy_step = 0
        self._initial_render()

    def _initial_render(self):
        print()  # Reserve a line for the progress bar

    def busy(self):
        self.isbusy = True

    def notbusy(self):
        self.isbusy = False

    def start(self):
        self._render()

    def update(self, amount=1):
        if self.isbusy:
            self._render()
            return
        self.current += amount
        if self.current > self.total:
            self.current = self.total
        self._render()

    def finish(self):
        self.current = self.total
        self.isbusy = False
        self._render(final=True)

    def makeModernLogging(self, process_name):
        from .ModernLogging import ModernLogging
        return ModernLogging(process_name)

    def logging(self, message, level="INFO", modernLogging=None):
        with ModernProgressBar._lock:
            # ログ行数をリセット
            self.log_lines = 0

            if modernLogging is None:
                modernLogging = self.makeModernLogging(self.process_name)
            result = modernLogging._make(message, level, self.process_color)
            
            # ログメッセージをプログレスバーの上に表示
            if self.log_lines > 0:
                move_up = self.log_lines
            else:
                move_up = len(ModernProgressBar._active_bars) - self.index
            sys.stdout.write(f"\033[{move_up}A")  # 上に移動
            sys.stdout.write("\033[K")  # 現在の行をクリア
            print(result)
            
            self.log_lines += 1  # ログ行数を増やす
            
            # プログレスバーを再描画
            self._render()

    def _render(self, final=False):
        progress = self.current / self.total
        bar = self._progress_bar(progress)
        percentage = f"{progress:.2%}"
        status = "[DONE]" if final else f"[{self.current}/{self.total}]"
        line = f"{self.process_name} - ({self._color(self.process_color)}{bar}{self._color("reset")}) {percentage} {status}"
        
        # ログ行数を考慮してプログレスバーの位置を調整
        total_move_up = self.log_lines + (len(ModernProgressBar._active_bars) - self.index)
        sys.stdout.write(f"\033[{total_move_up}A")  # 上に移動
        sys.stdout.write("\033[K")  # 行をクリア
        print(line)
        # カーソルをログの下（プログレスバーの下）に戻す
        sys.stdout.write(f"\033[{total_move_up}B")
        sys.stdout.flush()

    def _progress_bar(self, progress):
        bar_length = 20
        if not self.isbusy:
            empty_bar = "-"
            if self.current == self.total:
                center_bar = ""
            else:
                center_bar = "-"
            filled_bar = "-"
            if self.current == self.total:
                filled_length = int(progress * bar_length) + 1
            else:
                filled_length = int(progress * bar_length)
            return f"{self._color("blue")}{filled_bar * filled_length}{self._color("cyan")}{center_bar}{self._color("black")}{empty_bar * (bar_length - filled_length)}"
        else:
            busy_symbol_length = 1
            busy_end_bar_length = bar_length - self.busy_step
            busy_start_bar_length = bar_length - busy_end_bar_length
            self.busy_step = (self.busy_step + 1) % (bar_length + 1)
            return f"{self._color("black")}{"-" * busy_start_bar_length}{self._color("blue")}{"-" * busy_symbol_length}{self._color("black")}{"-" * busy_end_bar_length}"
        
    def _color(self, color_name):
        if color_name == "cyan":
            return self._color_by_code(36)
        elif color_name == "magenta":
            return self._color_by_code(35)
        elif color_name == "yellow":
            return self._color_by_code(33)
        elif color_name == "green":
            return self._color_by_code(32)
        elif color_name == "red":
            return self._color_by_code(31)
        elif color_name == "blue":
            return self._color_by_code(34)
        elif color_name == "white":
            return self._color_by_code(37)
        elif color_name == "black":
            return self._color_by_code(30)
        elif color_name == "reset":
            return self._color_by_code(0)
        else:
            return ""
             

    def _color_by_code(self, color_code):
        return f"\033[{color_code}m"
    
if __name__ == "__main__":
    progress_bar = ModernProgressBar(1000, "example process", 31)
    progress_bar.start()
    progress_bar.busy()
    for i in range(100):
        progress_bar.update()
        time.sleep(0.1)
    progress_bar.notbusy()
    for i in range(1000):
        progress_bar.update()
        time.sleep(0.1)
    progress_bar.finish()