import threading
import os
import socket
from DataService import DataService
from cryptography.fernet import Fernet

KEY = b"afcbXv_0yebyn2iJbbt_DDvQdec3f96ImNXLq-AAGT0="

MONITOR_POS_KEY = 0
MONITOR_POS_NAME = 1
MONITOR_POS_IP = 2
MONITOR_POS_ADMIN_KEY = 3


class serverThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr[0]  # ip

        this_folder = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(this_folder, f"files/{self.addr}.txt")

    def run(self):
        f = Fernet(KEY)
        if not os.path.isfile(self.path):
            with open(self.path, "x") as file:
                pass

        while True:
            with open(self.path, "a", encoding="utf-8") as file:
                try:
                    data = f.decrypt(self.conn.recv(4096).decode("utf-8"))
                    data = data.decode("utf-8")
                    file.write(f"{data} \n")
                except Exception as e:
                    print(e)
                    break


# server IP and PORT
IP = "0.0.0.0"
PORT = 8882


def main():
    """main function to start the server"""
    print("starting server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        thread_list = []
        data = DataService()
        try:
            while True:
                try:
                    s.listen(1)
                    conn, addr = s.accept()
                    print(f"Connect attpeted to server by {addr}")
                    if addr[0] in [
                        str(x[MONITOR_POS_IP]) for x in data.GetAllMonitorUsers()
                    ]:
                        print(f"Connectd")
                        x = serverThread(conn, addr)
                        x.start()
                        thread_list.append(x)
                    else:
                        print(f"connection from unknown - ignoring: {addr}")
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)
            for i in thread_list:
                i.join()


if __name__ == "__main__":
    main()
