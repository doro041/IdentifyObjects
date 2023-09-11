# This is the code for the leaderboard. It will link to a database that stores all the names, emails, and times of the players. It will then display the top 10 players and their times. When the leaderboard button is clicked, it will display the leaderboard.

# The leaderboard consists of a list of entries. Each entry has a name, time, and email. The list is sorted by time and displays the ranking in the list. The top 10 entries are displayed on the screen.

import tkinter as tk
from tkinter import ttk
from datetime import time
import DB  
import common

class LeaderboardDisplay:
    """This class represents the leaderboard display. It will display the top 10 entries in the leaderboard."""

    def __init__(self, master):
        self.window = master
        WIDTH = 800
        HEIGHT = 600
        self.window.title("Leaderboard")

       # Task bar section.
        taskBar = ttk.LabelFrame(self.window, width=WIDTH, height=HEIGHT * (10/100))
        taskBar.pack()

        # Back button section.
        backButton = ttk.Button(self.window, image=common.back_img, width=10, style='back.TButton', command=self.back)
        backButton.pack(side="bottom", pady=10)

        # Fetch leaderboard data from the database using the DB module
        leaderboard_data = DB.get_leaderboard_entries()

        # Create the Treeview widget and set it as an instance variable
        self.entries = ttk.Treeview(self.window, columns=(['Name', 'Time', 'Ranking']), show='headings')
        self.entries.heading('#1', text='Name')
        self.entries.heading('#2', text='Time')
        self.entries.heading('#3', text='Ranking')

        for rank, (username, score, timestamp) in enumerate(leaderboard_data, start=1):
            self.entries.insert(parent='', index='end', iid=rank, values=(username, score, timestamp))

        self.entries.pack(expand=True, fill="y")
        self.window.mainloop()

    def back(self):
        """A function that returns to the previous window."""
        common.release_win(self.window)

# TODO: Figure out how the styles might work with the new ttk components. 

# TODO: Make the back button have functionality by switching windows. 


def run(win):
    l = LeaderboardDisplay(win)
