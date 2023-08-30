#This is the code for the leaderboard. It will link to a database that stores all the names, emails, and times of the players. It will then display the top 10 players and their times. When the leaderboard button is clicked, it will display the leaderboard.

import tkinter as tk
window = tk.Tk()
""" WIDTH = 2560
HEIGHT = 1600 """
WIDTH = 800
HEIGHT = 600
window.geometry(f"{WIDTH}x{HEIGHT}")
window.title("Leaderboard")
window.maxsize(WIDTH, HEIGHT)
entries = tk.Frame(window, bg="#8e8e8e", width=WIDTH / 2, height=HEIGHT, relief="sunken", bd=1)
entries.pack(expand=True, fill="y", pady=10)


window.mainloop()