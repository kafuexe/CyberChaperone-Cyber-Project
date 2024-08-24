import customtkinter as ctk
from PIL import Image
from DataService import DataService
import os
import socket
from CTkMessagebox import CTkMessagebox


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


class SlidePanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, start_pos, end_pos, color):
        """initialize SlidePanel"""
        super().__init__(master=parent, fg_color=color)

        # general attributes
        self.parent = parent
        self.start_pos = start_pos - 0.02
        self.end_pos = end_pos
        self.width = abs(start_pos - end_pos)
        self.button_list = []

        # animation logic
        self.pos = self.end_pos
        self.in_start_pos = False
        self.rely = 0.2
        self.relheight = 0.8

        # layout
        self.place(
            relx=self.pos,
            rely=self.rely,
            relwidth=self.width,
            relheight=self.relheight,
        )
        ## adding buttons in update instead of here for login

    def animate(self):
        """choose how to animate the slide panel"""
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        """animate the slide panel to its forward position"""
        if self.pos > self.end_pos:
            self.pos -= 0.018
            self.place(
                relx=self.pos,
                rely=self.rely,
                relwidth=self.width,
                relheight=self.relheight,
            )
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        """animate the slide panel to its back position"""
        if self.pos < self.start_pos:
            self.pos += 0.018
            self.place(
                relx=self.pos,
                rely=self.rely,
                relwidth=self.width,
                relheight=self.relheight,
            )
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

    def add_button(self, person):
        """add a button to the side panel and connect it to a person"""

        button = ctk.CTkButton(
            master=self,
            text=person[MONITOR_POS_NAME],  # name
            font=FONT_BUTTON,
            fg_color=COLOR_ICON_BLUE,
            command=lambda person=person: self.parent.person_page(person),
            width=125,
            height=40,
            text_color=COLOR_TEXT_GREEN,
        )
        button.pack(pady=5)
        self.button_list.append(button)
        return button

    def clear(self):
        """destroy all buttons in the panel"""
        for button in self.button_list:
            button.destroy()
        self.button_list = []


class TopPanel(ctk.CTkFrame):
    def __init__(self, parent, sidePanel, color):
        """initialize the top panel"""
        super().__init__(master=parent, fg_color=color)
        self._fg_color = color
        self.master = parent
        menu_button = ctk.CTkButton(
            self,
            image=ctk.CTkImage(Image.open(r"assets/menu.png"), size=(90, 90)),
            text="",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=sidePanel.animate,
            width=95,
            height=95,
        )

        add_person_button = ctk.CTkButton(
            self,
            image=ctk.CTkImage(Image.open(r"assets/addPerson.png"), size=(90, 90)),
            text="",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=self.master.place_person_page,
            width=95,
            height=95,
        )
        my_account_button = ctk.CTkButton(
            self,
            image=ctk.CTkImage(Image.open(r"assets/account.png"), size=(90, 90)),
            text="",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=lambda: [
                self.master.login_page.place_page(),
                self.master.signup_page.move_destroy_page(),
            ],
            width=95,
            height=95,
        )

        menu_button.place(relx=0.08, rely=0.5, anchor="center")
        add_person_button.place(relx=0.22, rely=0.5, anchor="center")
        my_account_button.place(relx=0.92, rely=0.5, anchor="center")
        colored_box = ctk.CTkFrame(master=parent, fg_color=COLOR_TEXT_GREEN)
        colored_box.place(relx=-0.2, rely=0.19, relwidth=1.4, relheight=0.01)

        self.place(relx=0, rely=0, relwidth=1, relheight=0.19)


class AddPersonPage(ctk.CTkFrame):
    def __init__(self, parent):
        """initialize add person page"""
        super().__init__(master=parent, fg_color=COLOR_BACKGROUND_BLACK)
        self.master = parent

        self.add_new_person_label = ctk.CTkLabel(
            master=self,
            text="Add New Person",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color="white",
            corner_radius=3,
        )
        self.newName = ""

        self.enter_name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="Name",
        )
        self.enter_ip_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="ip address",
        )

        self.add_new_person_button = ctk.CTkButton(
            self,
            image=ctk.CTkImage(Image.open(r"assets/addPerson.png"), size=(90, 90)),
            text="",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=lambda: self.master.add_person(
                self.enter_ip_entry.get(), self.enter_name_entry.get()
            ),
            width=95,
            height=95,
        )

        self.add_new_person_label.place(rely=0.2, relx=0.2)

        self.enter_name_entry.place(rely=0.4, relx=0.2)
        self.enter_ip_entry.place(rely=0.5, relx=0.2)

        self.add_new_person_button.place(rely=0.6, relx=0.2)
        self.place(relx=-1.5, rely=0.2, relwidth=1.3, relheight=0.8)

    def place_page(self):
        """place the page"""
        self.place(relx=0, rely=0.2, relwidth=1.3, relheight=0.8)

    def destroy_page(self):
        """destroy the page"""
        self.place(relx=-1.5, rely=0.2, relwidth=1.3, relheight=0.8)


class PersonPage(ctk.CTkFrame):
    def __init__(self, parent, person):
        """create a new person page"""
        super().__init__(master=parent, fg_color=COLOR_BACKGROUND_BLACK)
        self.master = parent
        self.person = person
        self.visible = False

        self.person_label = ctk.CTkLabel(
            master=self,
            text=self.person[MONITOR_POS_NAME],
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_TITLE,
        )
        self.ip_label = ctk.CTkLabel(
            master=self,
            text=self.person[MONITOR_POS_IP],
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
        )

        self.delete_person_button = ctk.CTkButton(
            master=self,
            text="Delete",
            height=40,
            width=100,
            fg_color=COLOR_TEXT_RED,
            text_color=COLOR_TEXT_WHITE,
            font=FONT_BUTTON,
            command=lambda person=person: self.master.get_master().destroy_monitor(
                person
            ),
        )

        self.bar = ctk.CTkFrame(master=self, fg_color=COLOR_TEXT_GREEN)

        self.gray_frame1 = ctk.CTkFrame(
            master=self, width=600, height=70, fg_color=COLOR_BACKGROUND_GRAY
        )
        self.gray_frame2 = ctk.CTkFrame(
            master=self, width=600, height=70, fg_color=COLOR_BACKGROUND_GRAY
        )
        self.gray_frame3 = ctk.CTkFrame(
            master=self, width=600, height=70, fg_color=COLOR_BACKGROUND_GRAY
        )

        self.text_label = ctk.CTkLabel(
            master=self.gray_frame1,
            text="",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            text_color=COLOR_TEXT_WHITE,
            font=FONT_BUTTON,
        )
        self.window_label = ctk.CTkLabel(
            master=self.gray_frame2,
            text="",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            text_color=COLOR_TEXT_WHITE,
            font=FONT_BUTTON,
        )
        self.dns_label = ctk.CTkLabel(
            master=self.gray_frame3,
            text="",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            text_color=COLOR_TEXT_WHITE,
            font=FONT_BUTTON,
        )

        self.keyboard_picture = ctk.CTkLabel(
            master=self,
            text="",
            image=ctk.CTkImage(Image.open(r"assets/keyboard.png"), size=(100, 100)),
            width=95,
            height=95,
        )
        self.eye_picture = ctk.CTkLabel(
            master=self,
            text="",
            image=ctk.CTkImage(Image.open(r"assets/eye.png"), size=(100, 100)),
            width=95,
            height=95,
        )
        self.web_picture = ctk.CTkLabel(
            master=self,
            text="",
            image=ctk.CTkImage(Image.open(r"assets/web.png"), size=(100, 100)),
            width=95,
            height=95,
        )

        self.keyboard_picture.place(rely=0.35, relx=0.13)
        self.eye_picture.place(rely=0.55, relx=0.13)
        self.web_picture.place(rely=0.75, relx=0.13)

        self.gray_frame1.place(rely=0.4, relx=0.3)
        self.gray_frame2.place(rely=0.6, relx=0.3)
        self.gray_frame3.place(rely=0.8, relx=0.3)

        self.text_label.place(rely=0.5, relx=0.05)
        self.window_label.place(rely=0.5, relx=0.05)
        self.dns_label.place(rely=0.5, relx=0.05)

        self.person_label.place(rely=0.05, relx=0.12)
        self.bar.place(rely=0.17, relx=0.1, relwidth=0.4, relheight=0.005)
        self.ip_label.place(rely=0.19, relx=0.15)

        self.delete_person_button.place(relx=0.85, rely=0.1)

    def update_text(self, text):
        """Update the text label"""
        self.text_label.configure(text=text)

    def update_ip(self, text):
        """update the ip label"""
        self.ip_label.configure(text=text)

    def update_window_text(self, text):
        """update current window text"""
        self.window_label.configure(text=text)

    def update_dns_text(self, text):
        """update current dns request text"""
        self.dns_label.configure(text=text)

    def get_master(self):
        """return the master of the object as a fix to a .cget not working"""
        return self.master

    def place_page(self):
        """determines  if you need to place a page or destroy it"""
        if self.visible:
            self.move_destroy_page()
        else:
            self.move_place_page()

    def move_place_page(self):
        """places the page so you can see it"""
        self.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
        self.visible = True

    def move_destroy_page(self):
        """destroys the page so you wont see it"""
        self.place(relx=-1, rely=0.2, relwidth=1, relheight=0.8)
        self.visible = False


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent):
        """crates the login page"""
        super().__init__(master=parent, fg_color=COLOR_BACKGROUND_BLACK)
        self.master = parent
        self.visible = False
        self.name_label = ctk.CTkLabel(
            master=self,
            text="Name:",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.password_label = ctk.CTkLabel(
            master=self,
            text="Password:",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.enter_name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="Name:",
        )
        self.enter_password_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="Password:",
        )
        self.login_button = ctk.CTkButton(
            self,
            text="login",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=lambda: [
                self.master.login_func(
                    self.enter_name_entry.get(), self.enter_password_entry.get()
                ),
                self.login_mode(),
            ],
            width=95,
            height=95,
        )
        self.signup_button = ctk.CTkButton(
            self,
            text="signup",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=lambda: [self.master.signup_page.place_page(), self.place_page()],
            width=95,
            height=95,
        )

        self.user_name_label = ctk.CTkLabel(
            self,
            text="username",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.ip_label = ctk.CTkLabel(
            self,
            text="ip",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )

        self.logout_button = ctk.CTkButton(
            self,
            text="logout",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=lambda: [self.master.logout(), self.login_mode()],
            width=95,
            height=95,
        )

        self.login_mode()

    def place_page(self):
        """determines  if you need to place a page or destroy it"""
        if self.visible:
            self.move_destroy_page()
        else:
            self.move_place_page()

    def move_place_page(self):
        """places the page so you can see it"""

        self.place(relx=0, rely=0.2, relwidth=1.3, relheight=0.8)
        self.visible = True

    def move_destroy_page(self):
        """destroys the page so you wont see it"""
        self.place(relx=-1, rely=0.2, relwidth=1, relheight=0.8)
        self.visible = False

    def login_mode(self):
        """if not logged in, show the login page else show the user information page and logout option"""
        self.enter_password_entry.delete(0, last_index="end")
        if self.master.admin_user != None:

            self.name_label.place(relx=2, rely=2)
            self.password_label.place(relx=2, rely=2)
            self.enter_name_entry.place(relx=2, rely=2)
            self.enter_password_entry.place(relx=2, rely=2)
            self.login_button.place(relx=2, rely=2)
            self.signup_button.place(relx=2, rely=2)

            # show my login info and allow to logout
            temp_text = str(self.master.admin_user[1])
            self.user_name_label.configure(text=temp_text)
            self.user_name_label.place(rely=0.20, relx=0.1)
            self.ip_label.place(rely=0.5, relx=0.4)
            self.ip_label.configure(text=self.get_ip())
            self.logout_button.place(relx=0.4, rely=0.7)

            pass
        else:
            self.user_name_label.place(relx=2, rely=2)
            self.ip_label.place(relx=2, rely=2)
            self.logout_button.place(relx=2, rely=2)

            # show login page
            self.name_label.place(rely=0.20, relx=0.1)
            self.password_label.place(rely=0.40, relx=0.1)

            self.enter_name_entry.place(rely=0.2, relx=0.35)
            self.enter_password_entry.place(rely=0.40, relx=0.35)
            self.login_button.place(rely=0.8, relx=0.5)
            self.signup_button.place(relx=0.2, rely=0.8)

    def get_ip(self):
        """gets the ip associated with the server"""
        try:
            hostname = socket.gethostname()
            ipv4_address = socket.gethostbyname(hostname)
            return ipv4_address
        except socket.gaierror:
            return "There was an error resolving the hostname."
        except Exception as e:
            return f"An unexpected error occurred: {e}"


class SignUpPage(ctk.CTkFrame):
    def __init__(self, parent):
        """Initializes the SignUp page"""
        super().__init__(master=parent, fg_color=COLOR_BACKGROUND_BLACK)
        self.master = parent
        self.visible = False
        self.name_label = ctk.CTkLabel(
            master=self,
            text="Name:",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.password_label = ctk.CTkLabel(
            master=self,
            text="Password:",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.password_check_label = ctk.CTkLabel(
            master=self,
            text="Password:",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_GREEN,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.enter_name_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="Name:",
        )
        self.enter_password_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="Password:",
        )
        self.enter_password_check_entry = ctk.CTkEntry(
            master=self,
            width=200,
            height=25,
            fg_color=COLOR_BACKGROUND_GRAY,
            placeholder_text="Password:",
        )
        self.signup_button = ctk.CTkButton(
            self,
            text="signup",
            fg_color=COLOR_BACKGROUND_GRAY,
            command=lambda: [self.signup()],
            width=95,
            height=95,
        )
        self.warning_label = ctk.CTkLabel(
            master=self,
            text="",
            width=120,
            height=25,
            fg_color=COLOR_BACKGROUND_BLACK,
            text_color=COLOR_TEXT_RED,
            font=FONT_BUTTON,
            anchor="w",
            justify="left",
        )
        self.name_label.place(rely=0.1, relx=0.1)
        self.password_label.place(rely=0.2, relx=0.1)
        self.password_check_label.place(rely=0.3, relx=0.1)

        self.enter_name_entry.place(rely=0.1, relx=0.3)
        self.enter_password_entry.place(rely=0.2, relx=0.3)
        self.enter_password_check_entry.place(rely=0.3, relx=0.3)

        self.signup_button.place(rely=0.5, relx=0.5)
        self.warning_label.place(relx=0.2, rely=0.6)

    def place_page(self):
        """determines  if you need to place a page or destroy it"""
        if self.visible:
            self.move_destroy_page()
        else:
            self.move_place_page()

    def move_place_page(self):
        """places the page so you can see it"""
        self.place(relx=0, rely=0.2, relwidth=1.3, relheight=0.8)
        self.visible = True

    def move_destroy_page(self):
        """destroys the page so you wont see it"""
        self.place(relx=-1, rely=0.2, relwidth=1, relheight=0.8)
        self.visible = False

    def signup(self):
        """sings up the user"""
        print(
            self.enter_name_entry.get(),
            self.enter_password_entry.get(),
            self.enter_password_check_entry.get(),
        )
        worked = self.master.signup_func(
            self.enter_name_entry.get(),
            self.enter_password_entry.get(),
            self.enter_password_check_entry.get(),
        )

        if worked:
            self.warning_label.configure(text="account crated")
            
        else:
            self.warning_label.configure(text="Username already exists")
            


from FileToGui import ClientFileThread


class BackPanel(ctk.CTkFrame):
    # all of this just to workaround .cget method not working on ctk objects
    def __init__(self, parent):
        """crates a back panel"""
        super().__init__(master=parent, fg_color=COLOR_BACKGROUND_BLACK)

    def get_master(self):
        """returns the master as a fix for .cget not working in ctk"""
        return self.master


class App(ctk.CTk):
    def __init__(self):
        """starts the application"""
        super().__init__(fg_color=COLOR_BACKGROUND_BLACK)
        self.geometry("900x640")
        self.title("CyberChaperone")
        self.db = DataService()
        self.db.create_tables()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.admin_user = None
        self.monitor_list = []
        self.person_page_List = []
        self.thread_list = []

        # all of this just to workaround .cget method not working on ctk
        self.back_panel = BackPanel(self)
        self.back_panel.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.signup_page = SignUpPage(self)
        self.login_page = LoginPage(self)

        self.add_person_panel = AddPersonPage(self)

        self.side_panel = SlidePanel(self, 0, -0.25, COLOR_BACKGROUND_GRAY)
        self.top_panel = TopPanel(self, self.side_panel, COLOR_BACKGROUND_GRAY)

        self.add_person_page_visibility = False
        # button

    def login_func(self, name, password):
        """Login function, that handles the login and starts threads"""
        temp_admin_user = self.db.check_login(name, password)
        if self.admin_user == None and temp_admin_user != None:
            self.admin_user = temp_admin_user
            self.monitor_list = self.db.get_monitor_list_by_admin_key(
                self.admin_user[0]
            )
            self.login_page.place_page()
            for monitor in self.monitor_list:
                self.add_monitor(monitor)

    def add_person(self, name, ip):
        """Add a new person to the list and the database, crates the new needed gui and threads and starts them"""
        if self.admin_user == None:
            return

        monitor = self.db.add_monitor_user(name, ip, self.admin_user[0])
        # updating list
        self.monitor_list = self.db.get_monitor_list_by_admin_key(self.admin_user[0])
        self.add_monitor(monitor)

    def add_monitor(self, monitor):
        monitor_button = self.side_panel.add_button(monitor)
        monitor_PersonPage = PersonPage(self.back_panel, monitor)
        self.person_page_List.append((monitor, monitor_PersonPage, monitor_button))
        thread = ClientFileThread(monitor, monitor_PersonPage)
        thread.start()
        self.thread_list.append(thread)

    def destroy_monitor(self, monitor):
        """deletes a monitor user after issuing a warning"""
        msg = CTkMessagebox(
            master=self,
            width=400,
            height=40,
            title="Warning!",
            message=f"Are you sure you want to DELETE {monitor[MONITOR_POS_NAME]}",
            option_1="Yes",
            option_2="Yes(keep Logs)",
            option_3="Cancel",
            fg_color=COLOR_BACKGROUND_GRAY,
            button_color=COLOR_TEXT_RED,
            text_color=COLOR_TEXT_WHITE,
            font=FONT_NORMAL_TEXT,
            option_focus="Cancel",
        )

        response = msg.get()

        if response == "Cancel" or response == None:
            return
        if response == "Yes":
            this_folder = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(this_folder, f"files/{monitor[MONITOR_POS_IP]}.txt")
            if os.path.isfile(path):
                os.remove(path)

        for x in self.person_page_List:
            if x[0][MONITOR_POS_KEY] == monitor[MONITOR_POS_KEY]:
                x[1].destroy()
                x[2].destroy()
                self.person_page_List.remove(x)
                self.db.delete_monitor_by_key(monitor[MONITOR_POS_KEY])
                break

        for thread in self.thread_list:
            if thread.monitor[MONITOR_POS_KEY] == monitor[MONITOR_POS_KEY]:
                thread.stop()
                break

    def place_person_page(self):
        """"""
        if not self.add_person_page_visibility:
            self.add_person_panel.place_page()
        else:
            self.add_person_panel.destroy_page()
        self.add_person_page_visibility = not self.add_person_page_visibility

    def person_page(self, person):
        """placing the presence page of by the key of the person"""
        for monitor, panel, button in self.person_page_List:
            if monitor[MONITOR_POS_KEY] == person[MONITOR_POS_KEY]:
                panel.place_page()
            else:
                panel.move_destroy_page()

    def logout(self):
        """logs out and clears all info from gui, stops unneeded threads"""
        for x in self.thread_list:
            x.stop()
        self.side_panel.clear()
        self.thread_list = []
        self.monitor_list = []
        self.admin_user = None

    def signup_func(self, name, password, password_check):
        """signup a user to db after checking user input"""
        if password != password_check and [len(name) > 0 and len(password) > 0]:
            return False

        return self.db.addAdminUser(name, password)

    def on_closing(self):
        """closes the application"""
        print("-----------------CLOSING--------------")
        for x in self.thread_list:
            x.stop()

        self.destroy()
        exit()
