import sqlite3
from tkinter import *
import main
from utils import DB_NAME, Utils

class CustomerInfo:
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_frames()
        self._create_widgets()

    def _setup_window(self):
        """Set up the main window properties."""
        pad = 3
        self.root.title("CUSTOMER INFO")
        self.root.geometry(
            "{0}x{1}+0+0".format(self.root.winfo_screenwidth() - pad, self.root.winfo_screenheight() - pad)
        )

    def _create_frames(self):
        """Create frames for the layout."""
        self.top_frame = Frame(self.root)
        self.top_frame.pack(side="top")

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side="top")

        self.left_frame = Frame(self.root, relief="solid")
        self.left_frame.pack(side="left")

        self.right_frame = Frame(self.root, relief="solid")
        self.right_frame.pack(side="left")

    def _create_widgets(self):
        """Create and place all widgets."""
        # Display title
        Utils.create_label(
            self.top_frame, "LIST OF GUESTS", font=('arial', 50, 'bold'), fg="#15d3ba", anchor="center", row=0, column=3
        )

        # Name section
        Utils.create_label(
            self.left_frame, "NAME", font=('arial', 20, 'bold'), fg="#15d3ba", anchor="center", row=0, column=1
        )
        self.name_customer_entry = Utils.create_text_field(self.left_frame, height=30, width=70, row=1, column=1)

        # Room number section
        Utils.create_label(
            self.right_frame, "ROOM NO", font=('arial', 20, 'bold'), fg="#15d3ba", anchor="center", row=0, column=1
        )
        self.room_no_customer_entry = Utils.create_text_field(self.right_frame, height=30, width=70, row=1, column=1)

        # Buttons
        Utils.create_button(
            self.top_frame, "HOME", main.home_ui, row=8, column=3
        )
        Utils.create_button(
            self.top_frame, "DISPLAY", self._display_info, row=8, column=4
        )
    
    def _display_info(self):
        """Fetch and display customer information."""
        # Fetch customer names and room numbers using Utils
        guests = Utils.get_all_guests()

        # Display customer names
        self.name_customer_entry.delete(1.0, END)
        self.room_no_customer_entry.delete(1.0, END)
        for guest in guests:
            self.name_customer_entry.insert(INSERT, guest[0] + '\n')
            self.room_no_customer_entry.insert(INSERT, str(guest[4]) + '\n')
        if not guests:
            self.name_customer_entry.insert(INSERT, "NO GUESTS FOUND\n")
            self.room_no_customer_entry.insert(INSERT, "NO GUESTS FOUND\n")

def customer_info_ui():
    root = Tk()
    application = CustomerInfo(root)
    root.mainloop()