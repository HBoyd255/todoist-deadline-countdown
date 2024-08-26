import tkinter as tk
import random
import webbrowser
from typing import List
from todoist_api_python.models import Task

PAD_X = 0
PAD_Y = 0
CHOSEN_FONT = "Roboto Slab"


"""2-Bit colours
White      224,248,208
Light Gray 136,192,112
Dark Gray   52,104, 86
Black        8, 24, 32
"""

WHITE = "#e0f8d0"
LIGHT_GRAY = "#88c070"
DARK_GRAY = "#346856"
BLACK = "#081820"

TEXT_COLOR = BLACK

class GUI:
    def __init__(self, get_data_function) -> None:

        self._get_data_function = get_data_function

        self._root = tk.Tk()
        self._root.title("Todoist Task Selector")
        self._root.geometry("400x400")
        self._root.configure(bg=WHITE)

    def _show_deadline_list(self):
        """Shows a table of key-value pairs as labels, fitting within the 400x400 window."""

        # Clear the main window.
        for widget in self._root.winfo_children():
            widget.destroy()

        # Create a frame with a border to hold the table
        table_frame = tk.Frame(
            self._root,
            bg=WHITE,
            bd=5,  # Border width
            relief="solid",  # Border style
        )
        table_frame.pack(fill=tk.BOTH, expand=True, padx=PAD_X, pady=PAD_Y)

        # Configure columns to expand and fill space
        table_frame.grid_columnconfigure(0, weight=5, uniform="col")
        table_frame.grid_columnconfigure(1, weight=1, uniform="col")

        # Create table headers
        tk.Label(
            table_frame,
            text="Task",
            font=(CHOSEN_FONT, 24),
            bg=DARK_GRAY,
            fg=TEXT_COLOR,
            bd=1,
            relief="solid",
        ).grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        tk.Label(
            table_frame,
            text="Days",
            font=(CHOSEN_FONT, 24),
            bg=DARK_GRAY,
            fg=TEXT_COLOR,
            bd=1,
            relief="solid",
        ).grid(row=0, column=1, padx=PAD_X, pady=PAD_Y, sticky="nsew")

        # For each task, create a row with the task name and days until deadline.
        for i, (key, value) in enumerate(self._data.items(), start=1):

            even_row = i % 2 == 0

            if even_row:
                colour_a = WHITE
                colour_b = LIGHT_GRAY
            else:
                colour_a = LIGHT_GRAY
                colour_b = WHITE

            tk.Label(
                table_frame,
                text=key,
                font=(CHOSEN_FONT, 20),
                bg=colour_a,
                fg=TEXT_COLOR,
                bd=1,
                relief="solid",
            ).grid(row=i, column=0, padx=PAD_X, pady=PAD_Y, sticky="nsew")

            tk.Label(
                table_frame,
                text=value,
                font=(CHOSEN_FONT, 20),
                bg=colour_b,
                fg=TEXT_COLOR,
                bd=1,
                relief="solid",
            ).grid(row=i, column=1, padx=PAD_X, pady=PAD_Y, sticky="nsew")

    def _start(self):
        """Initializes the GUI by getting the data and showing the context menu."""

        self._data = self._get_data_function()

        self._show_deadline_list()

    def _show_loading_screen(self):
        initial_frame = tk.Frame(self._root, bg=WHITE)
        initial_frame.pack(fill=tk.BOTH, expand=True)

        initial_label = tk.Label(
            initial_frame,
            text="Loading...",
            font=(CHOSEN_FONT, 16),
            bg=WHITE,
            fg=TEXT_COLOR,
        )
        initial_label.pack(pady=PAD_Y, expand=True)

    def run(self):

        self._show_loading_screen()

        self._root.after(200, self._start)

        # Start the Tkinter event loop
        self._root.mainloop()
