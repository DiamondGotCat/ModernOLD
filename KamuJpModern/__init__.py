import sys

class KamuJpModern:
    def __init__(self):
        pass

    def color(self, color_code):
        return f"\033[{color_code}m"
    
    def modernLogging(self, process_name):
        from .ModernLogging import ModernLogging
        return ModernLogging(process_name)
    
    def modernProgressBar(self, total, process_name, process_color=32):
        from .ModernProgressBar import ModernProgressBar
        return ModernProgressBar(total, process_name, process_color)

if __name__ == "__main__":
    import time

    logger = KamuJpModern().modernLogging("main")
    logger.log("This is a test message", "INFO")
    logger.log("This is a warning message", "WARNING")
    logger.log("This is an error message", "ERROR")
    logger.log("This is a debug message", "DEBUG")

    progress_bar1 = KamuJpModern().modernProgressBar(100, "Task 1", 32)
    progress_bar2 = KamuJpModern().modernProgressBar(200, "Task 2", 34)

    progress_bar1.start()
    progress_bar2.start()

    for i in range(100):
        time.sleep(0.05)
        progress_bar1.update()

    for i in range(100):
        time.sleep(0.05)
        progress_bar2.update(2)

    progress_bar1.finish()
    progress_bar2.finish()

