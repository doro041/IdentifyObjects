from tkinter import * 
import tkinter as tk 
from tkinter.ttk import Label
from PIL import ImageTk, Image
from subprocess import call


import common

import tkinter as tk

# Global window reference
win = None

# Stops main window loop and destroys window items when moving to next section
def create_window():
    win.quit()
    common.release_win(win)

def run(root):
    global win
    win = root
    text=Text(root)
    #Sets the main text onto the window, any alterations that need to be made to the main has to happen here
    label = tk.Label(root, text="Ready to Win Big? Join the AI Societys Spot-the-Difference Challenge! \n\n 1. Sign Up- Enter your name and email- no passwords needed \n\n 2. Start the Game! - Click the 'Start' button to view 2 images side by side and find the differences \n\n Selection\n\nPress to start drawing rectangle\nThen press to release\nIf you don't like what you've drawn, press the 'u' key or the escape key\n\n\n 3. Beat the Timer- Finish the puzzles as quick as possible to get on the leaderboard! \n\n We hope you enjoy the game, and Good Luck!",
                 bg='black',fg="white", font=("Arial",30), justify='center') # You can use use color names instead of color codes.
    #Sets the properties for the button, any changes to the button that need to be made need to be made here, will make the button look better and larger with more readable text
    click_here = tk.Button(root, image=common.start_img,
                       bg='black',fg="white", activebackground="black", activeforeground="white", padx = 10, pady = 5, borderwidth=0, highlightthickness=0, command=create_window)


    #Centers the main text
    label.pack(padx=10, pady=10, fill="both", expand=True)
    click_here.pack(padx=10, pady=10,expand=True)

    #Below the code is displaying the logo
    img= common.logo
    #Places the image onto the main window
    imgLabel=Label(root, image=img, background="black")
    imgLabel.pack()
    #Positions the logo to the top left hand side
    imgLabel.place(x=10, y=10, anchor= "nw")
    root.title('Spot the difference')
    #Will edit the inital size of the root window as my screen doesnt work well for testing at the specified 2560 × 1600
    root.configure(bg='black')
    root.mainloop()
