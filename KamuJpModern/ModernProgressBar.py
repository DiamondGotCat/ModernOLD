import sys
import threading

class ModernProgressBar:
    _active_bars = []
    _last_rendered = False
    _lock = threading.Lock()

    def __init__(self, total, process_name, process_color):
        self.total = total
        self.current = 0
        self.process_name = process_name
        self.process_color = process_color
        self.index = len(ModernProgressBar._active_bars)
        ModernProgressBar._active_bars.append(self)
        self.log_lines = 0
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
        line = f"{self.process_name} - ({self._color(self.process_color)}{bar}{self._color(0)}) {percentage} {status}"
        
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
        empty_bar = "/"
        filled_bar = "-"
        filled_length = int(progress * bar_length)
        return f"{filled_bar * filled_length}{empty_bar * (bar_length - filled_length)}"

    def _color(self, color_code):
        return f"\033[{color_code}m"