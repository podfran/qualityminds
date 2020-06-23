import time

from wrapt_timeout_decorator import timeout


@timeout(15, use_signals=False)
def is_file_downloaded(download_file_path):
    while True:
        if download_file_path.is_file():
            return True
        time.sleep(1)
