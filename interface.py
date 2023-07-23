"""Primary GUI interface"""
import os
import tkinter as tk
import pickle
import consts as c
from connection_automator.bot_controller import BotController

class Interface:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LinkedIn Connect")
        self.root.geometry("350x150")  # Set initial window size
        self.root.resizable(False, False)  # Disable window resizing
        
        blank = tk.Label(self.root)
        blank.pack()
        
        self.connect_button = tk.Button(self.root, text="Automate Connections",
                                        command=self.open_connect_page,
                                        width=20)
        self.connect_button.pack(pady=0)

        self.search_message = ""
        self.connect_message = ""

    def open_connect_page(self):
        try:
            saved_inputs = "connection_automator/data/saved_connect_inputs.pkl"
            with open (saved_inputs, 'rb') as file:
                saved_settings = pickle.load(file)
        except:
            pass
        # Function to open the Connection Automator page
        connect_page = tk.Toplevel(self.root)
        connect_page.title("Automate Connections")
        connect_page.geometry("300x610")  # Set window size
        connect_page.resizable(False, False) 

        # Set LinkedIn frame
        linkedin_frame = tk.LabelFrame(connect_page, text="LinkedIn")
        linkedin_frame.pack(pady=10)

        # LinkedIn username and password labels and entry boxes
        user_label = tk.Label(linkedin_frame, text="LinkedIn Username:")
        user_label.pack(pady=5)
        user_entry = tk.Entry(linkedin_frame)
        user_entry.pack(padx=6)
        try:
            user_entry.insert(0, saved_settings[0])
        except:
            pass

        password_label = tk.Label(linkedin_frame, text="LinkedIn Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(linkedin_frame, show="*")
        password_entry.pack(padx=6, pady=5)

        # Set filters frame
        filters_frame = tk.LabelFrame(connect_page, text="Filters")
        filters_frame.pack(pady=10)

        # Connection message label and entry box
        con_msg_label = tk.Label(filters_frame, text="Connection Message:")
        con_msg_label.pack(pady=5)
        con_msg_entry= tk.Entry(filters_frame)
        con_msg_entry.pack(pady=5)
        try:
            con_msg_entry.insert(0, saved_settings[1])
        except:
            pass

        # Number of requests to send label entry box
        num_req_label = tk.Label(filters_frame, 
                                 text="Number of requests to send:")
        num_req_label.pack(pady=5)
        num_req_entry = tk.Entry(filters_frame)
        num_req_entry.pack()
        try:
            num_req_entry.insert(0, saved_settings[2])
        except:
            pass

        # Minimum connection count label and entry box
        min_label = tk.Label(filters_frame, 
                             text="Minimum connections count:")
        min_label.pack(pady=5)
        min_entry = tk.Entry(filters_frame)
        min_entry.pack(padx=6, pady=5)
        try:
            min_entry.insert(0, saved_settings[3])
        except:
            pass

        # Set advanced frame
        adv_frame = tk.LabelFrame(connect_page, text="Advanced")
        adv_frame.pack(pady=10)

        # Excel file path label and entry box
        exl_label = tk.Label(adv_frame, text="Excel file path:")
        exl_label.pack(pady=5)
        exl_entry = tk.Entry(adv_frame)
        exl_entry.pack(pady=5)
        try:
            exl_entry.insert(0, saved_settings[4])
        except:
            pass

        # Set message label
        self.connect_msg_label = tk.Label(connect_page, text="")
        self.connect_msg_label.pack(pady=5)

        # Set Connect button
        search_button = tk.Button(connect_page, text="Connect", width=20,
                    command=lambda: self.from_connect_gui(user_entry.get(),
                                                        password_entry.get(),
                                                        con_msg_entry.get(),
                                                        num_req_entry.get(),
                                                        min_entry.get(),
                                                        exl_entry.get()))
        search_button.pack(pady=10)


    def display_search_message(self):
        self.search_msg_label.config(text=self.search_message, 
                                     wraplength=300, height=1)
        self.search_msg_label.update()

    def display_connect_message(self):
        self.connect_msg_label.config(text=self.connect_message, 
                                      wraplength=300, height=1)
        self.connect_msg_label.update()

    def from_connect_gui(self, user, password, msg, num, min, excel_path):
        self.save_connect_settings(user, msg, num, min, excel_path)
        connect = True
        try:
            if user !="":
                c.USERNAME = user
            else: 
                connect = False
                self.connect_message = "Username must not be blank."
                self.display_connect_message()
                raise ValueError
            
            if password != "":
                c.PASSWORD = password
            else: 
                connect = False
                self.connect_message = "Password must not be blank."
                self.display_connect_message()
                raise ValueError
            
            if len(msg) <= 300:
                c.MESSAGE = msg
            else:
                connect = False
                self.connect_message = "Message must be less than 300 chars."
                self.display_connect_message()
                raise ValueError

            if num.isnumeric() and 1 <= int(num) <= 50:
                c.NUM_REQUESTS = int(num)
            else: 
                connect = False
                self.connect_message = "Num requests must be between 1 and 50."
                self.display_connect_message()
                raise ValueError

            if min.isnumeric() and 0<= int(min) <= 500:
                c.MINIMUM_CONNECTION_COUNT = int(min)
            else: 
                connect = False
                self.connect_message = "Min connections must be between 0 and 500."
                self.display_connect_message()
                raise ValueError

            end = excel_path[-4:] == 'xlsx'
            if os.path.exists(excel_path) and end:
                c.EXCEL_INPUT_LOCATION = excel_path
            else:
                connect = False
                self.connect_message = "Invalid Excel file location."
                self.display_connect_message()
                raise ValueError
            
            if connect:
                self.connect_message = "Connecting: Do not close window!"
                self.display_connect_message()
                controller = BotController()
                self.connect_message = controller.run()
                self.display_connect_message()

        except ValueError:
            pass

    def save_connect_settings(self, user, msg, num, min, excel_path):
        settings = [user,msg,num,min,excel_path]
        with open ("connection_automator/data/saved_connect_inputs.pkl", 
                   'wb') as file:
            pickle.dump(settings, file)

    def run(self):
        """
        Launches the GUI application.
        """
        self.root.mainloop()