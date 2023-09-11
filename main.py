import tkinter as tk
import common

import StartScreen
import registrypage
import identifyobj
import leaderboard

common.win = tk.Tk()
win = common.win
win.title("Spot The Difference")
win["bg"] = "black"
win.attributes('-fullscreen', True)
win.geometry('2560x1600')

win.protocol("WM_DELETE_WINDOW", common.close_win)

common.init()

win.iconphoto(False, common.logo)

while True:
    StartScreen.run(win)
    name = registrypage.run(win)
    score, time = identifyobj.run(win)
    leaderboard.run(win)

win.destroy()
print(f"Name: {name}, score: {score}, time: {time}")
