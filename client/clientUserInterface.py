import customtkinter as ctk
import os
import ipaddress
from CTkMessagebox import CTkMessagebox
import socket


COLOR_TEXT_RED = "#FF0000"
COLOR_BACKGROUND_BLACK = "#212121"
COLOR_BACKGROUND_GRAY = "#323232"
COLOR_ICON_BLUE = "#0D738F"
COLOR_TEXT_GREEN = "#4BE4C5"
COLOR_TEXT_WHITE = "#FFFFFF"

FONT_BUTTON = ("italic", 20)
FONT_TITLE = ("italic", 60)
FONT_NORMAL_TEXT = ("italic", 20)
MONITOR_POS_KEY = 0
MONITOR_POS_NAME = 1
MONITOR_POS_IP = 2
MONITOR_POS_ADMIN_KEY = 3


class ClientApp(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=COLOR_BACKGROUND_BLACK)
        self.geometry("350x600")
        self.title("CyberChaperone Client")
        self.my_ip_label = ctk.CTkLabel(
            master=self,
            text=f"my ip address: \n {self.get_ip()}",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.ip_label = self.PersonLabel = ctk.CTkLabel(
            master=self,
            text="Server Ip:",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )

        self.ip_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="",
        )
        self.set_button = ctk.CTkButton(
            self,
            text="Set IP Address",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=lambda: self.SetIp(self.ip_entry.get()),
            width=95,
            height=95,
        )
        self.success_label = ctk.CTkLabel(
            master=self,
            text=f"",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.success_label.place(rely=0.5, relx=0.1)
        self.my_ip_label.place(rely=0.20, relx=0.32)
        self.ip_label.place(rely=0.40, relx=0.05)

        self.ip_entry.place(rely=0.40, relx=0.35)
        self.set_button.place(rely=0.8, relx=0.3)

    def SetIp(self, ip):
        if not self.checkIp(ip):
            msg = CTkMessagebox(
                master=self,
                width=400,
                height=40,
                title="Error!",
                message=f"Invalid IP address",
                option_1="Ok",
                fg_color=COLOR_BACKGROUND_GRAY,
                button_color=COLOR_ICON_BLUE,
                text_color=COLOR_BACKGROUND_BLACK,
                font=FONT_NORMAL_TEXT,
            )
            return

        this_folder = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(this_folder, f"settings.txt")
        with open(filename, "w") as file:
            file.write(ip)
        self.success_label.configure(text="successfully changed ip")

    def checkIp(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def get_ip(self):
        try:
            hostname = socket.gethostname()
            ipv4_address = socket.gethostbyname(hostname)
            return ipv4_address
        except socket.gaierror:
            return "There was an error resolving the hostname."
        except Exception as e:
            return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()
