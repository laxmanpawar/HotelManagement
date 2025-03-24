from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox  # Import Combobox
import sqlite3
import main
from utils import DB_NAME, Utils


class CheckIN:
    def __init__(self, root):
        self.root = root
        self.available_rooms, self.occupied_rooms = Utils.get_available_rooms()
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        

    def _setup_window(self):
        """Set up the main window properties."""
        pad = 3
        self.root.title("CHECK IN")
        self.root.geometry(
            "{0}x{1}+0+0".format(self.root.winfo_screenwidth() - pad, self.root.winfo_screenheight() - pad)
        )

    def _create_frames(self):
        """Create frames for the layout."""
        self.top = LabelFrame(self.root)
        self.top.pack(side="top")

        self.checkinFrame = Frame(self.root)
        self.checkinFrame.pack(side="top")

        self.buttonsFrame = Frame(self.root)
        self.buttonsFrame.pack(side="top")

    def _create_widgets(self):
        """Create and place all widgets."""
        # Display message
        Utils.create_label(self.top, "CHECK IN", font=('arial', 50, 'bold'), fg="#15d3ba", anchor="w", row=0, column=3)

        # TODO: Fix binding of the Input fields
        self.name_var = StringVar()
        self.address_var = StringVar()
        self.mobile_var = StringVar()  # Use StringVar for mobile to handle validation
        self.days_var = IntVar()

        self.nameEntry = Utils.create_input_field(self.checkinFrame, "ENTER YOUR NAME :", self.name_var, row=0)
        self.addressEntry = Utils.create_input_field(self.checkinFrame, "ENTER YOUR ADDRESS :", self.address_var, row=1)
        self.mobileEntry = Utils.create_input_field(self.checkinFrame, "ENTER YOUR MOBILE NUMBER :", self.mobile_var, row=2)
        self.daysEntry = Utils.create_input_field(self.checkinFrame, "ENTER NUMBER OF DAYS TO STAY :", self.days_var, row=3, is_int=True)

        # Room number selection
        if self.available_rooms:
            self.room_number_var = StringVar()
            Utils.create_label(self.checkinFrame, "SELECT ROOM NUMBER: ", font=('arial', 20, 'bold'), fg="#15d3ba", anchor="w", row=4, column=2)
            self.room_combobox = Combobox(self.checkinFrame, values=self.available_rooms, textvariable=self.room_number_var, state="readonly", width=47)
            self.room_combobox.grid(row=4, column=3, padx=10, pady=10)
            self.room_combobox.current(0)  # Set the first available room as default
            self.room_number_var.set(self.available_rooms[0])  # Set default value in StringVar
        else:
            self.room_number_var = None
            messagebox.showerror("ERROR", "NO ROOMS AVAILABLE")

        # Buttons
        Utils.create_button(self.buttonsFrame, "SUBMIT", self._submit_info, row=5, column=1)
        Utils.create_button(self.buttonsFrame, "HOME", main.home_ui, row=5, column=2)
        Utils.create_button(self.buttonsFrame, "RESET", self._reset, row=5, column=3)

    def _submit_info(self):
        """Handle the submission of check-in information."""
        room_number = self.room_combobox.get()
        if not room_number:
            messagebox.showerror("ERROR", "NO ROOMS AVAILABLE")
            return

        name = self.nameEntry.get()
        address = self.addressEntry.get()
        mobile = self.mobileEntry.get()
        days = self.daysEntry.get()

        if not Utils.validate_mobile(mobile) or not Utils.validate_days(days):
            return

        conn = sqlite3.connect(DB_NAME)
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO Hotel (FullName, Address, mobile_number, number_days, room_number) VALUES (?, ?, ?, ?, ?)',
                (name, address, mobile, days, room_number)
            )
            conn.commit()
        self._reset_fields()

    def _reset(self):
        """Reset the form fields."""
        self._reset_fields()

    def _reset_fields(self):
        """Clear all input fields and reset the room selection."""
        # Reset the StringVar and IntVar variables
        self.nameEntry.delete(0, END)
        self.addressEntry.delete(0, END)
        self.mobileEntry.delete(0, END)
        self.daysEntry.delete(0, END)

        # Reset the room selection in the Combobox
        self.available_rooms, self.occupied_rooms = Utils.get_available_rooms()
        if self.available_rooms:
            self.room_combobox['values'] = self.available_rooms
            self.room_combobox.current(0)  # Reset to the first available room
            self.room_number_var.set(self.available_rooms[0])  # Update the StringVar for the room
        else:
            self.room_number_var.set("")  # Clear the room number if no rooms are available
            messagebox.showerror("ERROR", "NO ROOMS AVAILABLE")

def check_in_ui_fun():
    root = Tk()
    application = CheckIN(root)
    root.mainloop()