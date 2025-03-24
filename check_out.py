import sqlite3
from tkinter import *
from tkinter.ttk import Combobox
import main
from utils import DB_NAME, Utils

class CheckOut:
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_frames()
        self._create_widgets()

    def _setup_window(self):
        """Set up the main window properties."""
        pad = 3
        self.root.title("CHECK OUT")
        self.root.geometry(
            "{0}x{1}+0+0".format(self.root.winfo_screenwidth() - pad, self.root.winfo_screenheight() - pad)
        )

    def _create_frames(self):
        """Create frames for the layout."""
        self.top_frame = Frame(self.root)
        self.top_frame.pack(side="top")

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side="top")

        self.info_frame = Frame(self.root)
        self.info_frame.pack(side="top")

    def _create_widgets(self):
        """Create and place all widgets."""
        # Display message
        Utils.create_label(self.top_frame, "CHECK OUT", font=('arial', 50, 'bold'), fg="#15d3ba", anchor="center", row=0, column=3)

        # Room number input
        Utils.create_label(
            self.bottom_frame, "SELECT THE ROOM NUMBER :", font=('arial', 20, 'bold'), fg="#15d3ba", anchor="center", row=2, column=2
        )

        # Fetch occupied rooms from the database
        available_rooms, occupied_rooms = Utils.get_available_rooms()

        # Create Combobox for room selection
        self.room_var = StringVar()
        self.room_no_combobox = Combobox(self.bottom_frame, textvariable=self.room_var, values=occupied_rooms, state="readonly", width=10)
        self.room_no_combobox.grid(row=2, column=3, padx=10, pady=10)
        if len(occupied_rooms) > 0:
            self.room_no_combobox.current(0)  # Set the first available room as default 
            self.room_no_combobox.set(occupied_rooms[0])  # Set default value in StringVar
        else:
            self.room_no_combobox.set('N/A')
            self.room_no_combobox.set('')  # Set default value in StringVar

        # Information display
        self.get_info_entry = Text(self.info_frame, height=15, width=90)
        self.get_info_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        Utils.create_button(
            self.bottom_frame, "CHECK OUT", self._check_out, row=3, column=2
        )
        Utils.create_button(
            self.bottom_frame, "HOME", main.home_ui, row=3, column=3
        )

    def _check_out(self):
        """Handle the check-out process."""
        room_number = self.room_var.get()
        if not room_number:
            self.get_info_entry.insert(INSERT, "PLEASE SELECT A VALID ROOM NUMBER\n")
            return

        conn = sqlite3.connect(DB_NAME)
        with conn:
            cursor = conn.cursor()

            cursor.execute("SELECT room_number FROM Hotel")
            rooms = [row[0] for row in cursor.fetchall()]

            if int(room_number) in rooms:
                cursor.execute("SELECT Fullname, room_number FROM Hotel WHERE room_number = ?", (room_number,))
                result = cursor.fetchone()
                if result:
                    self.get_info_entry.insert(
                        INSERT, f"\n{result[0]} has checked out from room {result[1]}\n"
                    )
                    cursor.execute("DELETE FROM Hotel WHERE room_number = ?", (room_number,))
                    conn.commit()
            else:
                self.get_info_entry.insert(INSERT, "PLEASE SELECT A VALID ROOM NUMBER\n")


def check_out_ui():
    root = Tk()
    application = CheckOut(root)
    root.mainloop()