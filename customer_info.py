import sqlite3
from tkinter import *
import main
from utils import DB_NAME

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
        self._create_label(
            self.top_frame, "LIST OF CUSTOMER", font=('arial', 50, 'bold'), fg="#15d3ba", row=0, column=3
        )

        # Name section
        self._create_label(
            self.left_frame, "NAME", font=('arial', 20, 'bold'), fg="#15d3ba", row=0, column=1
        )
        self.name_customer_entry = self._create_text_field(self.left_frame, height=30, width=70, row=1, column=1)

        # Room number section
        self._create_label(
            self.right_frame, "ROOM NO", font=('arial', 20, 'bold'), fg="#15d3ba", row=0, column=1
        )
        self.room_no_customer_entry = self._create_text_field(self.right_frame, height=30, width=70, row=1, column=1)

        # Buttons
        self._create_button(
            self.top_frame, "HOME", main.home_ui, row=8, column=3
        )
        self._create_button(
            self.top_frame, "DISPLAY", self._display_info, row=8, column=4
        )

    def _create_label(self, parent, text, font, fg, row, column):
        """Helper method to create a label."""
        label = Label(parent, font=font, text=text, fg=fg, anchor="center")
        label.grid(row=row, column=column, padx=10, pady=10)

    def _create_text_field(self, parent, height, width, row, column):
        """Helper method to create a text field."""
        text_field = Text(parent, height=height, width=width)
        text_field.grid(row=row, column=column, padx=10, pady=10)
        return text_field

    def _create_button(self, parent, text, command, row, column):
        """Helper method to create a button."""
        button = Button(
            parent, text=text, font=('', 15), bg="#15d3ba", relief=RIDGE, height=2, width=15,
            fg="black", anchor="center", command=command
        )
        button.grid(row=row, column=column, padx=10, pady=10)

    def _display_info(self):
        """Fetch and display customer information."""
        conn = sqlite3.connect(DB_NAME)
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS Hotel (Fullname TEXT, Address TEXT, mobile_number TEXT, number_days TEXT, room_number NUMBER)'
            )
            conn.commit()

            # Fetch and display customer names
            cursor.execute("SELECT Fullname FROM Hotel")
            names = cursor.fetchall()
            self.name_customer_entry.delete(1.0, END)  # Clear previous data
            for name in names:
                self.name_customer_entry.insert(INSERT, name[0] + '\n')

            # Fetch and display room numbers
            cursor.execute("SELECT room_number FROM Hotel")
            rooms = cursor.fetchall()
            self.room_no_customer_entry.delete(1.0, END)  # Clear previous data
            for room in rooms:
                self.room_no_customer_entry.insert(INSERT, str(room[0]) + '\n')


def customer_info_ui():
    root = Tk()
    application = CustomerInfo(root)
    root.mainloop()