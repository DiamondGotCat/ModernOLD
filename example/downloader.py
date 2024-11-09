import argparse
import requests
import os
import time
from KamuJpModern import KamuJpModern

class Downloader:
    ONE_MB = 1024 * 1024

    def __init__(self):
        self.total_downloaded = 0
        self.progress_bar = KamuJpModern().modernProgressBar(
            total=0,
            process_name="Downloading",
            process_color=32
        )
        self.start_time = time.time()
        self.logger = KamuJpModern().modernLogging(process_name="Downloader")

    def get_file_size(self, url):
        try:
            response = requests.head(url, allow_redirects=True)
            response.raise_for_status()
            file_size = int(response.headers.get('Content-Length', 0))
            if file_size == 0:
                raise ValueError("Content-Length is zero or not provided.")
            return file_size
        except (requests.RequestException, ValueError):
            response = requests.get(url, stream=True)
            response.raise_for_status()
            file_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file_size += len(chunk)
            return file_size

    def on_unit_downloaded(self, bytes_downloaded):
        elapsed_time = time.time() - self.start_time
        total_downloaded_mb = self.total_downloaded / self.ONE_MB
        elapsed_time_formatted = time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time))
        log_message = f"{total_downloaded_mb:.2f} MB downloaded in {elapsed_time_formatted}"
        self.progress_bar.logging(log_message)

    def download_file(self, url, output_path):
        file_size = self.get_file_size(url)
        if file_size == 0:
            print("Failed to get file size.")
            return
        unit_multiplier = self.ONE_MB
        total_units = file_size / unit_multiplier
        self.progress_bar.total = total_units
        self.progress_bar.start()
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error occurred during download: {e}")
            return
        downloaded = 0
        self.total_downloaded = 0 
        self.start_time = time.time()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    chunk_size = len(chunk)
                    downloaded += chunk_size
                    self.total_downloaded += chunk_size
                    self.on_unit_downloaded(downloaded)
                    self.progress_bar.update(downloaded / unit_multiplier)
                    downloaded = 0
            if downloaded > 0:
                self.on_unit_downloaded(downloaded)
        self.progress_bar.finish()

    def main(self):
        parser = argparse.ArgumentParser(description='Download File')
        parser.add_argument('url', help='URL of the file to download')
        parser.add_argument('output', help='Path to save the downloaded file')
        args = parser.parse_args()
        self.logger.log("Downloading started!")
        self.download_file(args.url, args.output)
        self.logger.log("Download finished!")

if __name__ == '__main__':
    downloader = Downloader()
    downloader.main()
