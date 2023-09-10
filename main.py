import tkinter as tk
import common

import StartScreen
import registrypage
import identifyobj

common.win = tk.Tk()
win = common.win
win.title("Spot The Difference")
win["bg"] = "black"

win.bind("WM_DELETE_WINDOW", common.close_win)

common.init()

win.iconphoto(False, common.logo)

StartScreen.run(win)
name = registrypage.run(win)

score, time = identifyobj.run(win)

print(f"Name: {name}, score: {score}, time: {time}")
