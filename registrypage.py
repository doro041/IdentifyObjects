import tkinter as tk
from tkinter import ttk

import common

win = None
name_entry = None
email_entry = None

name = None # might need name for later

def register_user():
    global name
    # Get the user-entered data
    name = name_entry.get()
    email = email_entry.get()

    print(f"Registered User:\nName: {name}\nEmail: {email}")
    # register user
    # ...
    
    common.release_win(win)


def run(root):
    global win
    global name_entry
    global email_entry
    win = root

    canvas = tk.Canvas(root, bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)




    # Create the frame for the main content
    frame = tk.Frame(canvas, bg="black")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Load and display the logo image with custom width and height
    logo_image = common.logo
    logo_label = tk.Label(frame, image=logo_image, bg="black")
    logo_label.pack(anchor="nw", padx=10, pady=10)

    # Create and style the "Name" input field
    name_entry = ttk.Entry(frame, font=("Helvetica", 16), width=80)
    name_entry.insert(0, "Name")
    name_entry.pack(ipadx=10, ipady=15, padx=10, pady=30, anchor="w") 
    name_entry.config(style="Custom.TEntry")  # Apply custom styling

    # Create and style the "Email" input field
    email_entry = ttk.Entry(frame, font=("Helvetica", 16), width=80)
    email_entry.insert(0, "Email")
    email_entry.pack(ipadx=10, ipady=15, padx=10, pady=30, anchor="w") 
    email_entry.config(style="Custom.TEntry")  # Apply custom styling

    # Create a "Register" button as an image 
    register_image = common.next_img
    register_button = tk.Button(frame, image=register_image, command=register_user, relief="flat", borderwidth=0)
    register_button.image = register_image  
    register_button.pack(padx=10, pady=(5, 20))


    style = ttk.Style()
    style.configure("Custom.TEntry", borderwidth=1, relief="solid", background="#D9D9D9")

    root.mainloop()
    return name
