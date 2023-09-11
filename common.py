import tkinter as tk

# logo image
logo = None
# next button image
next_img = None
# window
win = None
# start button image
start_img = None

# load the images
def init():
    global logo
    global next_img
    global start_img
    logo = tk.PhotoImage(file="images/AILOGO.png")
    next_img = tk.PhotoImage(file="images/NextButton.png")
    start_img = tk.PhotoImage(file="images/StartButton.png")

# https://stackoverflow.com/questions/15995783/how-to-delete-all-children-elements for destroying all of a window's widgets
# releases the window from a section
def release_win(win: tk.Tk):
    win.quit()
    for widget in win.winfo_children():
        widget.destroy()
# https://stackoverflow.com/questions/71917396/error-tkinter-tclerror-cant-invoke-wm-command-application-has-been-destroy for not good solution of wrapping in try except 
# 
# basic close window callback for nothing to happen on window closing -> override if want something special
def close_win():
    global win
    global running
    win.destroy()
    exit(0)
