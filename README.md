<img width="499" alt="Screenshot" src="https://github.com/user-attachments/assets/b8cf83ed-23f5-4dd5-8e68-a84842b62fad">

Modern is a simple package for logging and progress bar and More!

## Installation

```bash
pip install kamu-jp-modern
```

## Usage

```python
from KamuJpModern import KamuJpModern
```

### Logging

```python
logger = KamuJpModern().modernLogging(process_name="main")
logger.log("This is a test message", "INFO")
```

### Progress Bar

```python
progress_bar = KamuJpModern().modernProgressBar(total=100, process_name="Task 1", process_color=32)
progress_bar.start()

for i in range(100):
  time.sleep(0.05)
  progress_bar.update()

progress_bar.finish()
```
