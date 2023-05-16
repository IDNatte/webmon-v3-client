import threading
import requests
import sys
import os


class UploaderThread(threading.Thread):
    def __init__(self, upload_folder, url, token):
        super().__init__()

        self.upload_file = self.__file_selector(upload_folder)
        self.upload_folder = upload_folder
        self.stop_event = threading.Event()
        self.url = url

        self._result = None
        self.headers = {"Authorization": f"Bearer {token}"}

    def run(self):
        test = os.path.join(self.upload_folder, self.upload_file)
        with open(test, "rb") as data:
            try:
                files = {"file": data}
                response = requests.post(self.url, headers=self.headers, files=files)
                self._result = response.json()

            except (
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ConnectionError,
            ) as net_error:
                self._result = str(net_error)
                sys.exit()

    def stop(self):
        self.stop_event.set()

    def get_result(self):
        return self._result

    def __file_selector(self, upload_path):
        upload_path = [
            f
            for f in os.listdir(upload_path)
            if os.path.isfile(os.path.join(upload_path, f))
        ]

        upload_target = sorted(upload_path, reverse=True)[0]

        return upload_target
