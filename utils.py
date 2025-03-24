from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox  # Import Combobox

DB_NAME = 'Hotel.db'


class Utils:
    @staticmethod
    def create_button(parent, text, command, row, column):
        """Helper method to create a button."""
        button = Button(
            parent, text=text, font=('', 15), bg="#15d3ba", relief=RIDGE, height=2, width=15,
            fg="black", anchor="center", command=command
        )
        button.grid(row=row, column=column, padx=10, pady=10)

    @staticmethod
    def create_label(parent, text, font, fg, anchor, row, column):
        """Helper method to create a label."""
        label = Label(parent, font=font, text=text, fg=fg, anchor=anchor)
        label.grid(row=row, column=column, padx=10, pady=10)

    @staticmethod
    def create_text_field(parent, height, width, row, column):
        """Helper method to create a text field."""
        text_field = Text(parent, height=height, width=width)
        text_field.grid(row=row, column=column, padx=10, pady=10)
        return text_field

    @staticmethod
    def create_input_field(parent, label_text, variable, row, is_int=False, validate_command=None):
        """Helper method to create an input field with a label."""
        Utils.create_label(parent, label_text, font=('arial', 20, 'bold'), fg="#15d3ba", anchor="w", row=row, column=2)
        entry = Entry(parent, width=50, textvariable=variable)  # Properly bind the variable
        entry.grid(row=row, column=3, padx=10, pady=10)
        if is_int and validate_command:
            entry.config(validate="key", validatecommand=validate_command)
        return entry

    @staticmethod
    def validate_mobile(mobile):
        """Validate mobile number."""
        if len(str(mobile)) == 10:
            return True
        messagebox.showerror("ERROR", "PLEASE ENTER A 10-DIGIT MOBILE NUMBER")
        return False

    @staticmethod
    def validate_days(days):
        """Validate number of days."""
        if str(days).isdigit():
            return True
        messagebox.showerror("ERROR", "NUMBER OF DAYS MUST BE A POSITIVE INTEGER")
        return False