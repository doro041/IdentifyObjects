import tkinter as tk

# logo image
logo = None
# next button image
next_img = None
# window
win = None

# load the images
def init():
    global logo
    global next_img
    logo = tk.PhotoImage(file="images/AILOGO.png")
    next_img = tk.PhotoImage(file="images/NextButton.png")

# https://stackoverflow.com/questions/15995783/how-to-delete-all-children-elements for destroying all of a window's widgets
# releases the window from a section
def release_win(win: tk.Tk):
    win.quit()
    for widget in win.winfo_children():
        widget.destroy()

# basic close window callback for nothing to happen on window closing -> override if want something special
def close_win():
    global win
    win.destroy()
    exit(0)
