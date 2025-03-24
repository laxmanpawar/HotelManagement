import sqlite3
from tkinter import *
import main
import utils
from utils import DB_NAME, Utils

class RoomwiseInfo:
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_frames()
        self._create_widgets()

    def _setup_window(self):
        """Set up the main window properties."""
        pad = 3
        self.root.title("ROOM INFORMATION")
        self.root.geometry(
            "{0}x{1}+0+0".format(self.root.winfo_screenwidth() - pad, self.root.winfo_screenheight() - pad)
        )

    def _create_frames(self):
        """Create frames for the layout."""
        self.top_frame = Frame(self.root)
        self.top_frame.pack(side="top")

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side="top")

        self.info_frame = Frame(self.root, width=454, height=20)
        self.info_frame.pack(side="top")

        self.button_frame = Frame(self.root)
        self.button_frame.pack(side="top")

    def _create_widgets(self):
        """Create and place all widgets."""
        # Display title
        Utils.create_label(self.top_frame, "INFORMATION OF CUSTOMER", font=('arial', 50, 'bold'), fg='#15d3ba', anchor='center', row=0, column=3)

        # Room number input
        self.room_number_var = IntVar()
        Utils.create_label(self.bottom_frame, "ENTER THE ROOM NUMBER:", font=('arial', 20, 'bold'), fg="#15d3ba", anchor='center', row=2, column=2)
        self.room_no_entry = Entry(self.bottom_frame, width=5, textvariable=self.room_number_var)
        self.room_no_entry.grid(row=2, column=3, padx=10, pady=10)

        # Information display
        self.info_text = Utils.create_text_field(self.info_frame, height=15, width=90, row=1, column=1)

        # Buttons
        Utils.create_button(self.button_frame, "SUBMIT", self._fetch_room_info, row=8, column=2)
        Utils.create_button(self.button_frame, "HOME", main.home_ui, row=8, column=3)

    def _fetch_room_info(self):
        """Fetch and display room information based on the entered room number."""
        try:
            room_number = self.room_number_var.get()
        except ValueError:
            self.info_text.insert(INSERT, "PLEASE ENTER A VALID ROOM NUMBER\n")
            return

        conn = sqlite3.connect(DB_NAME)
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS Hotel (Fullname TEXT, Address TEXT, mobile_number TEXT, number_days TEXT, room_number NUMBER)'
            )
            conn.commit()

            cursor.execute("SELECT room_number FROM Hotel")
            rooms = [row[0] for row in cursor.fetchall()]

            if room_number in rooms:
                cursor.execute("SELECT * FROM Hotel WHERE room_number = ?", (room_number,))
                result = cursor.fetchone()
                if result:
                    self.info_text.delete(1.0, END)  # Clear previous data
                    self.info_text.insert(
                        INSERT,
                        f"NAME: {result[0]}\nADDRESS: {result[1]}\nMOBILE NUMBER: {result[2]}\n"
                        f"NUMBER OF DAYS: {result[3]}\nROOM NUMBER: {result[4]}\n"
                    )
            else:
                self.info_text.insert(INSERT, "PLEASE ENTER A VALID ROOM NUMBER\n")


def get_info_ui():
    root = Tk()
    application = RoomwiseInfo(root)
    root.mainloop()