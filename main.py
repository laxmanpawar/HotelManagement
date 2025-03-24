from tkinter import *
import check_in_ui
import check_out
import RoomwiseInfo
import customer_info

class Hotel:
    def __init__(self, root):
        self.root = root
        self._setup_window()
        self._create_frames()
        self._create_widgets()

    def _setup_window(self):
        """Set up the main window properties."""
        pad = 3
        self.root.title("HOTEL MANAGEMENT SYSTEM")
        self.root.geometry(
            "{0}x{1}+0+0".format(self.root.winfo_screenwidth() - pad, self.root.winfo_screenheight() - pad)
        )

    def _create_frames(self):
        """Create frames for the layout."""
        self.top_frame = Frame(self.root)
        self.top_frame.pack(side="top")

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack(side="top")

    def _create_widgets(self):
        """Create and place all widgets."""
        # Display welcome message
        self._create_label(self.top_frame, "WELCOME", font=('arial', 50, 'bold'), fg="#15d3ba", row=0, column=3)

        # Create buttons
        self._create_button(
            self.bottom_frame, "CHECK IN", check_in_ui.check_in_ui_fun, row=0, column=2
        )
        self._create_button(
            self.bottom_frame, "CHECK OUT", check_out.check_out_ui, row=1, column=2
        )
        self._create_button(
            self.bottom_frame, "INFORMATION OF ROOMS", RoomwiseInfo.get_info_ui, row=2, column=2
        )
        self._create_button(
            self.bottom_frame, "INFORMATION OF ALL GUEST", customer_info.customer_info_ui, row=3, column=2
        )
        self._create_button(
            self.bottom_frame, "EXIT", quit, row=4, column=2
        )

    def _create_label(self, parent, text, font, fg, row, column):
        """Helper method to create a label."""
        label = Label(parent, font=font, text=text, fg=fg, anchor="center")
        label.grid(row=row, column=column)

    def _create_button(self, parent, text, command, row, column):
        """Helper method to create a button."""
        button = Button(
            parent, text=text, font=('', 20), bg="#15d3ba", relief=RIDGE, height=2,
            width=50, fg="black", anchor="center", command=command
        )
        button.grid(row=row, column=column, padx=10, pady=10)

def home_ui():
    root = Tk()
    application = Hotel(root)
    root.mainloop()


if __name__ == '__main__':
    home_ui()
