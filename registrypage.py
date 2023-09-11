import tkinter as tk
from tkinter import ttk
import common
import DB  

win = None
name_entry = None
email_entry = None

# Function to handle the click event in the Name Entry
def name_entry_click(event):
    if name_entry.get() == "Name":
        name_entry.delete(0, tk.END)  # Clear the placeholder text

# Function to handle the click event in the Email Entry
def email_entry_click(event):
    if email_entry.get() == "Email":
        email_entry.delete(0, tk.END)  # Clear the placeholder text

# Function to handle the focus out event in the Name Entry
def name_entry_focus_out(event):
    if not name_entry.get():
        name_entry.insert(0, "Name")  # Restore the placeholder text

# Function to handle the focus out event in the Email Entry
def email_entry_focus_out(event):
    if not email_entry.get():
        email_entry.insert(0, "Email")  # Restore the placeholder tex

def register_user():
    # Get the user-entered data
    name = name_entry.get()
    email = email_entry.get()

    # Check if the user already exists
    user_id = DB.register_user(name, email)
    
    if user_id is not None:
        print(f"Registered User:\nName: {name}\nEmail: {email}\nUser ID: {user_id}")
    else:
        print("User already exists with the same username or email.")
    
    common.release_win(win)

def run(root):
    global win
    global name_entry
    global email_entry
    win = root

    canvas = tk.Canvas(root, bg="black", borderwidth=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Create the frame for the main content
    frame = tk.Frame(canvas, bg="black")
    frame.place(relx=0.5, rely=0.5, relwidth=1.0, relheight=1.0, anchor="center")

    # Load and display the logo image with custom width and height
    logo_image = common.logo
    logo_label = tk.Label(frame, image=logo_image, bg="black")
    logo_label.pack(anchor="nw", padx=10, pady=10)
 # Create and style the "Name" input field with a placeholder
    name_entry = ttk.Entry(frame, font=("Helvetica", 16), width=80)
    name_entry.insert(0, "Name")  # Set "Name" as a placeholder
    name_entry.pack(anchor="center", ipadx=10, ipady=15, padx=10, pady=30)
    name_entry.config(style="Custom.TEntry")  # Apply custom styling
    name_entry.bind("<FocusIn>", name_entry_click)  # Bind click event
    name_entry.bind("<FocusOut>", name_entry_focus_out)  # Bind focus out event

    # Create and style the "Email" input field with a placeholder
    email_entry = ttk.Entry(frame, font=("Helvetica", 16), width=80)
    email_entry.insert(0, "Email")  # Set "Email" as a placeholder
    email_entry.pack(anchor="center", ipadx=10, ipady=15, padx=10, pady=30)
    email_entry.config(style="Custom.TEntry")  # Apply custom styling
    email_entry.bind("<FocusIn>", email_entry_click)  # Bind click event
    email_entry.bind("<FocusOut>", email_entry_focus_out)  # Bind focus out event

    # Create a "Register" button as an image

    # Create a "Register" button as an image
    register_image = common.next_img
    register_button = tk.Button(frame, image=register_image, command=register_user, relief="flat", borderwidth=0, highlightthickness=0, fg="white", bg="black", activebackground="black", activeforeground="white")
    register_button.image = register_image
    register_button.pack(padx=10, pady=(5, 20))

    style = ttk.Style()
    style.configure("Custom.TEntry", borderwidth=1, relief="solid", background="#D9D9D9")

    root.mainloop()

