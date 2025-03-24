import sqlite3
from tkinter import *
from tkinter.ttk import Combobox
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
        Utils.create_label(self.top_frame, "ROOMWISE INFORMATION", font=('arial', 50, 'bold'), fg='#15d3ba', anchor='center', row=0, column=3)

        # Room number input
        Utils.create_label(self.bottom_frame, "SELECT THE ROOM NUMBER:", font=('arial', 20, 'bold'), fg="#15d3ba", anchor='center', row=2, column=2)

        # Fetch occupied rooms from the database
        available_rooms, occupied_rooms = Utils.get_available_rooms()

        # Create Combobox for room selection
        self.room_number_var = StringVar()
        self.room_no_combobox = Combobox(self.bottom_frame, textvariable=self.room_number_var, values=occupied_rooms, state="readonly", width=10)
        self.room_no_combobox.grid(row=2, column=3, padx=10, pady=10)
        if len(occupied_rooms) > 0:
            self.room_no_combobox.current(0)  # Set the first available room as default 
            self.room_no_combobox.set(occupied_rooms[0])  # Set default value in StringVar
        else:
            self.room_no_combobox.set('N/A')
            self.room_no_combobox.set('')  # Set default value in StringVar

        # Information display
        self.info_text = Utils.create_text_field(self.info_frame, height=15, width=90, row=1, column=1)

        # Buttons
        Utils.create_button(self.button_frame, "SUBMIT", self._fetch_room_info, row=8, column=2)
        Utils.create_button(self.button_frame, "HOME", main.home_ui, row=8, column=3)

    def _fetch_room_info(self):
        """Fetch and display room information based on the selected room number."""
        room_number = self.room_no_combobox.get()
        if not room_number:
            self.info_text.insert(INSERT, "PLEASE SELECT A VALID ROOM NUMBER\n")
            return

        conn = sqlite3.connect(DB_NAME)
        with conn:
            cursor = conn.cursor()

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
                self.info_text.insert(INSERT, "PLEASE SELECT A VALID ROOM NUMBER\n")


def get_info_ui():
    root = Tk()
    application = RoomwiseInfo(root)
    root.mainloop()