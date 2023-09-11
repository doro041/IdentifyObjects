# This is the code for the leaderboard. It will link to a database that stores all the names, emails, and times of the players. It will then display the top 10 players and their times. When the leaderboard button is clicked, it will display the leaderboard.

# The leaderboard consists of a list of entries. Each entry has a name, time, and email. The list is sorted by time and displays the ranking in the list. The top 10 entries are displayed on the screen.

import tkinter as tk
from tkinter import ttk
from datetime import time

import common

class LeaderboardEntry:
    """This class represents an entry in the leaderboard. It consists of a name, time, and email, and multiple objects can be sorted by time."""

    def __init__(self, name: str, timeTaken: time, email: str) -> None:
        self.name = name
        self.time = timeTaken
        self.email = email

    def __eq__(self, other) -> bool:
        if (self.name == other.name and self.time == other.time):
            return True
        return False
    # less than, greater than, less or equal and greater or equal operator for establishing order + ranking.

    def __le__(self, other) -> bool:
        if (self.time <= other.time):
            return True
        return False

    def __ge__(self, other) -> bool:
        if (self.time >= other.time):
            return True
        return False

    def __lt__(self, other) -> bool:
        if (self.time < other.time):
            return True
        return False

    def __gt__(self, other) -> bool:
        if (self.time > other.time):
            return True
        return False

    def __str__(self) -> str:
        return f'{self.name} {self.time.strftime("%H:%M:%S")}'


class LeaderboardDisplay:
    """This class represents the leaderboard display. It will display the top 10 entries in the leaderboard."""

    def __init__(self, master):
        self.window = master
        """ WIDTH = 2560
        HEIGHT = 1600 """
        WIDTH = 800
        HEIGHT = 600
        self.window.title("Leaderboard")

        # Styling for the new ttk components.

        


        #Task bar section. 
        taskBar = ttk.LabelFrame(self.window, width=WIDTH,
                            height=HEIGHT * (10/100))
        taskBar.pack()
        # Back button section. 

        backButton = ttk.Button(self.window, image=common.back_img,
                                width=10, style='back.TButton', command=self.back)
        backButton.pack(side="bottom", pady=10)
        #Leaderboard entries section.

        entries = ttk.Treeview(self.window, columns=(['Name', 'Time', 'Ranking']), show='headings', selectmode='none')
        entries.heading('#1', text='Name')
        entries.heading('#2', text='Time')
        entries.heading('#3', text='Ranking')

        s = ttk.Style()
        s.configure('TLabelFrame', background='black')
        s.configure('TButton', foreground='white', background='black', borderwidth=0, highlightthickness=0)
        # found out about fieldbackground from https://stackoverflow.com/questions/18044860/how-to-change-the-background-color-of-a-treeview
        s.configure('Treeview', font=('Helvetica', 15), foreground='white', background='black', fieldbackground='black', borderwidth=0)
        # found out about Treeview.Heading style from https://stackoverflow.com/questions/63239295/changing-background-color-of-ttk-treeview-heading
        s.configure('Treeview.Heading', font=('Helvetica', 18), background='black', foreground='white', borderwidth=0)
        s.map('TButton', foreground=[('active', 'white')], background=[('active', 'black')])


        # Test if ranking works with the list. It should be sorted by time.

        test1 = LeaderboardEntry("Romina", time(
            hour=13, minute=14, second=31), "")
        test2 = LeaderboardEntry("Doro", time(
            hour=13, minute=14, second=32), "")
        test3 = LeaderboardEntry("Fraser", time(
            hour=00, minute=14, second=30), "")

        rankList = [test1, test2, test3]
        rankList.sort()

        # Need to add each entry into the frame with ranking.

        for i in range(len(rankList)):
            currentEntry = rankList[i]
            entries.insert(parent='', index='end', iid=i, values=(currentEntry.name, currentEntry.time.strftime("%H:%M:%S"), i+1))

        entries.pack(expand=True, fill="y")
        self.window.mainloop()

    def back(self):
        """A function that returns to the previous window."""
        common.release_win(self.window)

# TODO: Figure out how the styles might work with the new ttk components. 

# TODO: Make the back button have functionality by switching windows. 


def run(win):
    l = LeaderboardDisplay(win)
