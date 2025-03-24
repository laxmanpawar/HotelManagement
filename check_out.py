import sqlite3
from tkinter import *
import main
from utils import DB_NAME

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
        self._create_label(self.top_frame, "CHECK OUT", font=('arial', 50, 'bold'), fg="#15d3ba", row=0, column=3)

        # Room number input
        self.room_var = IntVar()
        self._create_label(
            self.bottom_frame, "ENTER THE ROOM NUMBER :", font=('arial', 20, 'bold'), fg="#15d3ba", row=2, column=2
        )
        self.room_no_entry = Entry(self.bottom_frame, width=5, textvariable=self.room_var)
        self.room_no_entry.grid(row=2, column=3, padx=10, pady=10)

        # Information display
        self.get_info_entry = Text(self.info_frame, height=15, width=90)
        self.get_info_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        self._create_button(
            self.bottom_frame, "CHECK OUT", self._check_out, row=3, column=2
        )
        self._create_button(
            self.bottom_frame, "HOME", main.home_ui, row=3, column=3
        )

    def _create_label(self, parent, text, font, fg, row, column):
        """Helper method to create a label."""
        label = Label(parent, font=font, text=text, fg=fg, anchor="center")
        label.grid(row=row, column=column, padx=10, pady=10)

    def _create_button(self, parent, text, command, row, column):
        """Helper method to create a button."""
        button = Button(
            parent, text=text, font=('', 15), bg="#15d3ba", relief=RIDGE, height=2, width=15,
            fg="black", anchor="center", command=command
        )
        button.grid(row=row, column=column, padx=10, pady=10)

    def _check_out(self):
        """Handle the check-out process."""
        try:
            room_number = int(self.room_no_entry.get())
        except ValueError:
            self.get_info_entry.insert(INSERT, "PLEASE ENTER A VALID ROOM NUMBER\n")
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
                cursor.execute("SELECT Fullname, room_number FROM Hotel WHERE room_number = ?", (room_number,))
                result = cursor.fetchone()
                if result:
                    self.get_info_entry.insert(
                        INSERT, f"\n{result[0]} has checked out from room {result[1]}\n"
                    )
                    cursor.execute("DELETE FROM Hotel WHERE room_number = ?", (room_number,))
                    conn.commit()
            else:
                self.get_info_entry.insert(INSERT, "PLEASE ENTER A VALID ROOM NUMBER\n")


def check_out_ui():
    root = Tk()
    application = CheckOut(root)
    root.mainloop()