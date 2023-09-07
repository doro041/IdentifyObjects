# This is the code for the leaderboard. It will link to a database that stores all the names, emails, and times of the players. It will then display the top 10 players and their times. When the leaderboard button is clicked, it will display the leaderboard.

#The leaderboard consists of a list of entries. Each entry has a name, time, and email. The list is sorted by time and displays the ranking in the list. The top 10 entries are displayed on the screen.

import tkinter as tk
from datetime import time



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
    #less than, greater than, less or equal and greater or equal operator for establishing order + ranking.
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
    def __init__(self, backWindow=1):
        window = tk.Tk()
        """ WIDTH = 2560
        HEIGHT = 1600 """
        WIDTH = 800
        HEIGHT = 600
        window.geometry(f"{WIDTH}x{HEIGHT}")
        window.title("Leaderboard")
        window.maxsize(WIDTH, HEIGHT)

        taskBar = tk.Frame(window, bg="#fff",height=HEIGHT * (10/100))
        taskBar.pack(fill="x")


        backButton = tk.Button(window, text="< Back", bg="#fff", width=10, height=2)
        backButton.pack(side="bottom", pady=10)


        entries = tk.Frame(window, bg="#8e8e8e", width=WIDTH * (80/100),
                        height=HEIGHT)
        entries.columnconfigure((0,2,4), weight=1, uniform="group1")
        entries.columnconfigure((1,3), weight=2)
        tk.Label(entries, text='Name:', anchor='w').grid(row=0, column=0, sticky='nsew')
        tk.Label(entries, text='Time:', anchor='w').grid(row=0, column=2, sticky='nsew')
        tk.Label(entries, text='Ranking:', anchor='w').grid(row=0, column=4, sticky='nsew')
        
        #Test if ranking works with the list. It should be sorted by time.

        test1 = LeaderboardEntry("Romina", time(hour=13, minute=14, second=31), "")
        test2 = LeaderboardEntry("Doro", time(hour=13, minute=14, second=32), "")
        test3 = LeaderboardEntry("Fraser", time(hour=00, minute=14, second=30), "")

        rankList = [test1, test2, test3]
        rankList.sort()

        #Need to add each entry into the frame with ranking.

        for i in range(len(rankList)):
            """ rankList[i].display(entries).grid(column=0, row=i) """
            currentEntry = rankList[i]
            print(currentEntry.name, currentEntry.time.strftime("%H:%M:%S"), i)

            nameLabel = tk.Label(entries, text=currentEntry.name, anchor="w")
            timeLabel = tk.Label(entries, text=currentEntry.time.strftime("%H:%M:%S"), anchor='w')
            rankingLabel = tk.Label(entries, text=str(i), anchor='w')

            nameLabel.grid(row=i+1, column=0, sticky='nsew')
            timeLabel.grid(row=i+1, column=2, sticky='nsew')
            rankingLabel.grid(row=i+1, column=4, sticky='nsew')

            



        entries.pack(expand=True, fill="y")
        window.mainloop()
   


l = LeaderboardDisplay()