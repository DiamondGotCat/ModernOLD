import argparse
import requests
import os
import time
from KamuJpModern import KamuJpModern

ONE_MB = 1024 * 1024
total_downloaded = 0

def get_file_size(url):
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

def download_file(url, output_path):
    file_size = get_file_size(url)
    if file_size == 0:
        print("Failed to get file size.")
        return

    unit_multiplier = ONE_MB

    # プログレスバーの初期化
    total_units = file_size / unit_multiplier
    progress_bar = KamuJpModern().modernProgressBar(
        total=total_units,
        process_name="Downloading",
        process_color=32
    )
    progress_bar.start()

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error occurred during download: {e}")
        return

    downloaded = 0
    total_downloaded = 0  # 総ダウンロード量を追跡
    start_time = time.time()  # ダウンロード開始時刻を記録
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                chunk_size = len(chunk)
                downloaded += chunk_size
                total_downloaded += chunk_size

                on_unit_downloaded(downloaded, progress_bar, total_downloaded, start_time)

                while downloaded >= unit_multiplier:
                    progress_bar.update(1)
                    downloaded -= unit_multiplier

        # 残りのダウンロード分を処理（単位未満）
        if downloaded > 0:
            on_unit_downloaded(downloaded, progress_bar, total_downloaded, start_time)
            # プログレスバーは更新しない

def on_unit_downloaded(bytes_downloaded, progress_bar, total_downloaded, start_time):
    elapsed_time = time.time() - start_time
    total_downloaded_mb = total_downloaded / ONE_MB
    elapsed_time_formatted = time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time))
    log_message = f"{total_downloaded_mb:.2f} MB downloaded in {elapsed_time_formatted} seconds"
    progress_bar.logging(log_message)

def main():
    parser = argparse.ArgumentParser(description='Download File')
    parser.add_argument('url', help='URL of the file to download')
    parser.add_argument('output', help='Path to save the downloaded file')
    args = parser.parse_args()
    
    download_file(args.url, args.output)

if __name__ == '__main__':
    main()
