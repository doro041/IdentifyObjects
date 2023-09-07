from tkinter import * 
import tkinter as tk 
import tkinter.font
from tkinter.ttk import Label
from PIL import ImageTk, Image
import os 

import tkinter as tk
#Creates the main screen to display the ob
root = tk.Tk()
#Creates a new window after the start button is clicked to change what the button shows we need to change the TopLevel and create a new window for root, will edit once all files have been placed together
def create_window():
    newWindow=Toplevel(root)
    newWindow.title("ExampleTitle")
    #Determines size of the new screen can change later
    newWindow.geometry("200x200")

text=Text(root)
#Sets the main text onto the window, any alterations that need to be made to the main has to happen here
label = tk.Label(root, text="Ready to Win Big? Join the AI Societys Spot-the-Difference Challenge! \n\n 1. Sign Up- Enter your name and email- no passwords needed \n\n 2. Start the Game! - Click the 'Start' button to view 2 images side by side and find the differences \n\n 3. Beat the Timer- Finish the puzzles as quick as possible to get on the leaderboard! \n\n We hope you enjoy the game, and Good Luck!",
                 bg='black',fg="white", font=("Arial",30), justify='center') # You can use use color names instead of color codes.
#Sets the properties for the button, any changes to the button that need to be made need to be made here, will make the button look better and larger with more readable text
click_here = tk.Button(root, text="Start!",
                       bg='green',fg="black", padx = 10, pady = 5, command=create_window)


#Centers the main text
label.pack(padx=10, pady=10, fill="both", expand=True)
click_here.pack(padx=5, pady=5,expand=True)

#Below the code is displaying the logo, current logo quaility is greatly reduced will look into fixing this
img = Image.open("Logo_Dark.png")
img=img.resize((200,200), Image.ANTIALIAS)
img= ImageTk.PhotoImage(img)
#Places the image onto the main window, currently doesnt place into the new window
imgLabel=Label(root, image=img)
imgLabel.pack()
#Positions the logo to the top left hand side
imgLabel.place(anchor= "nw")
root.title('Spot the difference')
#Will edit the inital size of the root window as my screen doesnt work well for testing at the specified 2560 × 1600
root.geometry('200x100')
root.iconbitmap('Logo_Dark.png')
root.configure(bg='black')

root.mainloop()