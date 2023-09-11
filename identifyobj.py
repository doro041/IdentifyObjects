import tkinter as tk
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from operator import itemgetter
import json
import random

import common

"""
Sources I (Fraser) have used (other than documentation)  I don't know Tkinter - Fraser
  https://www.geeksforgeeks.org/loading-images-in-tkinter-using-pil/ for using Pillow with Tkinter
  https://pythonguides.com/tkinter/ this also for working with Tkinter
  https://tkinterexamples.com/events/mouse/ for mouse events

  I think https://stackoverflow.com/questions/47852221/tkinter-after-method-executing-immediately for sorting out my timer. I originally thought I wasn't calling it as a function but I now think I was.
  https://stackoverflow.com/questions/9776718/how-do-i-stop-tkinter-after-function for the after_cancel function
  https://docs.python.org/3/howto/sorting.html for sorting the list and mentioning the itemgetter function
  https://www.geeksforgeeks.org/how-to-hide-recover-and-delete-tkinter-widgets/ for hiding the differences label while modifying it
  https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter for overriding the window close method
  https://docs.python.org/3/library/json.html for working with json in python
  https://stackoverflow.com/questions/14838635/quit-mainloop-in-python for exiting the window mainloop
  https://stackoverflow.com/questions/68882832/scrollable-buttons-in-tkinter for explaining that you can't scroll things in a frame - you need a canvas
  https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter for scrolling of tkinter widgets
  https://www.pythontutorial.net/tkinter/tkinter-pack/ for explaining the pack function
  https://stackoverflow.com/questions/4310489/how-do-i-remove-the-light-grey-border-around-my-canvas-widget for removing the canvas border
  https://obsessive-coffee-disorder.com/rgb-to-grayscale-using-cimg/ for explaining human colour perception
  https://coderslegacy.com/python/change-tkinter-window-icon/ for using iconphoto and that iconbitmap only supports png image files on certain platforms
  https://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding for unbind

  I would like to write my formal complaint against the sun which tried to blind me as I was writing my code
  Please don't comment on how I have basically treated squares and rectangles as the same shape
  I hope my commit with no changes isn't noticed
"""

# Colour Constants based on human colour perception
RedMul = 0.299 # For scoring how different pixels are (high means more noticable)
GreenMul = 0.587
BlueMul = 0.114
# These are for creating sensitivity boundaries (high means less noticable)
RedInvMul = 0.242
GreenInvMul = 0.123
BlueInvMul = 0.635

# keep reading from file until have all data
def read_all(file):
    text = ""
    buffer = file.read()
    while len(buffer) > 0:
        text += buffer
        buffer = file.read()
    return text

# converts seconds to str format in time in the format 0:00
def sec_to_time(time: int):
    if time > 599 or time < 0:
        return "?:??"
    return str(time // 60) + ":" + format(time % 60, "0=2")

# swaps a and b and returns as tuple
def swap(a, b):
    return (b, a)

# returns if box b0 is inside box b1
def box_inside(b0, b1):
    x00, y00 = b0[0]
    x01, y01 = b0[1]
    
    x10, y10 = b1[0]
    x11, y11 = b1[1]

    if x00 >= x10 and x01 <= x11 and y00 >= y10 and y01 <= y11:
        return True
    return False

# Holds solution data
class Solution:
    def __init__(self):
        self.sol = [(0, 0), (0, 0)] # Main solution
        self.alt = None # Alternative solution
        self.score = 0

# returns true if solution box is in right area
def check_sol_box(rec, x0, y0, x1, y1, leniance):
    # create inner and outer boxes so there can be some error
    inner_x0 = x0 + leniance
    inner_y0 = y0 + leniance
    inner_x1 = x1 - leniance
    inner_y1 = y1 - leniance
    if inner_x0 > inner_x1:
        inner_x0 = (x0 + x1) // 2 # use average middle pixel for both as is line
        inner_x1 = inner_x0
    if inner_y0 > inner_y1:
        inner_y0 = (y0 + y1) // 2
        inner_y1 = inner_y0
    outer_x0 = x0 - leniance
    outer_y0 = y0 - leniance
    outer_x1 = x1 + leniance
    outer_y1 = y1 + leniance
    if box_inside([(inner_x0, inner_y0), (inner_x1, inner_y1)], rec) and box_inside(rec, [(outer_x0, outer_y0), (outer_x1, outer_y1)]):
        return True
    return False


# calculates the score for the player leniance -> how far either side of axis error can be to still be rewarded points for solution. Score algorithm may change in future
def do_score(selections, solutions, time, leniance = 5):
    num_correct = 0 # how many of the solutions the player got right
    score = 0
    solutions_used = []
    for rec in selections:
        rec_solutions = []
        for i in range(len(solutions)):
            if i not in solutions_used:
                solution = solutions[i]
                x0, y0 = solution.sol[0]
                x1, y1 = solution.sol[1]
                if check_sol_box(rec, x0, y0, x1, y1, leniance):
                    rec_solutions.append(i) # possible solution
                elif solution.alt is not None:
                    x0, y0 = solution.alt[0]
                    x1, y1 = solution.alt[1]
                    if check_sol_box(rec, x0, y0, x1, y1, leniance):
                        rec_solutions.append(i)

        # select lowest scoring solution
        chosen = -1
        chosen_score = 1000000000 # don't add scores bigger than this
        for sol_index in rec_solutions:
            if solutions[sol_index].score < chosen_score:
                chosen = sol_index
                chosen_score = solutions[sol_index].score
        if chosen != -1:
            num_correct += 1
            solutions_used.append(chosen)
            score += solutions[sol_index].score
    if num_correct == len(solutions):
        score += time # time bonus for if have all solutions and there is time left
    return score
# solutions should be in the format [top_left_pixel, bottom_right_pixel, score] where score is the points for finding that difference

# Window options: scroll -> add scrolling support, human_vision -> add biases to colours based on human perception
# Not using human_vision, sensitivity of 20 is good. I advise using 110 if you are using it though.

# User Window for player's attempt
class UserWin:
    def __init__(self, win, orig_img: Image, changed_img: Image, num_differences: int, solutions, scroll: bool = False):
        # creates Tkinter window, sets background and creates array of squares drawn and where the first click was
        self.win = win
        self.win.title("Spot The Difference")
        self.squares = []
        self.start_click = None

        self.time_call = None # tkinter time call so can stop it if ongoing

        # set images for user to draw to
        self.orig_img = orig_img # the original images
        self.changed_img = changed_img
        self.square_orig = orig_img.copy() # original image with all the selected squares drawn on it (used so have less drawing to do when user draws squares)
        self.square_changed = changed_img.copy()
        self.drawn_orig = self.square_orig.copy() # have currently drawn images so can close them when drawing something else
        self.drawn_changed = self.square_changed.copy()
        self.orig_tk = ImageTk.PhotoImage(self.drawn_orig) # in format for Tk to render -> these will hold the currently drawn images but are redundant
        self.changed_tk = ImageTk.PhotoImage(self.drawn_changed)
        self.solutions = solutions

        self.time = 61 # time to run for +1s
        self.score = 0 # the player's score
        self.running = True # timer hasn't run out
        self.num_differences = num_differences # how many differences to look for (0 or less will turn off differences display)
        self.canvas = tk.Canvas(self.win, bg="black", borderwidth=0, highlightthickness=0) # use canvas as it supports scrolling
        self.base_frame = tk.Frame(self.canvas, bg="black") # have frame so can do neat grid layout
        self.canvas.create_window((0, 0), window=self.base_frame, anchor="nw", width=self.win.winfo_width())
        self.canvas.pack(side="left", fill="both", expand=True) # make sure canvas takes up whole window

        # have image frame for grid layout of images
        self.image_frame = tk.Frame(self.base_frame, bg="black")

        self.lower_bar = tk.Frame(self.image_frame, bg="black")
        self.lower_bar.grid(row=1, column=0, columnspan=3)

        # displaying things on the screen

        self.logo_label = tk.Label(self.base_frame, image=common.logo, bg="black")
        self.logo_label.pack(anchor="nw", padx=10, pady=10, side="left")

        self.time_label = tk.Label(self.image_frame, text=f"{sec_to_time(self.time)}", font=("arial", 30), bg="black", fg="white")
        self.time_label.grid(row=0, column=1)

        self.diff_sol_label = tk.Label(self.image_frame, text=f"", font=("arial", 30), bg="black", fg="magenta")

        if num_differences > 0:
            self.diff_sol_label["text"] = f"Differences: {num_differences}"
            self.diff_sol_label.grid(row=2, column=1)

        self.next_button = tk.Button(self.base_frame, image=common.next_img, borderwidth=0, highlightthickness=0, bg="black", fg="white", activebackground="black", activeforeground="white", command=self.next_clicked)
        self.next_button.pack(anchor="ne", padx=10, pady=30, side="right")

        # where the images are
        self.orig_label = tk.Label(self.lower_bar, image=self.orig_tk, bg="black")
        self.orig_label.grid(row=0, column=0, padx=20, pady=20)

        self.changed_label = tk.Label(self.lower_bar, image=self.changed_tk, bg="black")
        self.changed_label.grid(row=0, column=1, padx=20, pady=20)

        self.image_frame.pack(anchor="center", pady=max(60 + common.next_img.height(), 20 + common.logo.height()))
        # vertical scrollbar
        self.scroll = scroll
        if scroll:
            self.scroll_bar = tk.Scrollbar(self.win, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scroll_bar.set)
            self.scroll_bar.pack(side="right", fill="y")

        # events for images and the window
        self.orig_label.bind("<Button-1>", self.img_clicked)
        self.orig_label.bind("<Motion>", self.img_move)
        self.changed_label.bind("<Button-1>", self.img_clicked)
        self.changed_label.bind("<Motion>", self.img_move)
        self.image_frame.bind("<Configure>", self.config_base)
        self.win.bind("<Key>", self.key_pressed)
        self.win.protocol("WM_DELETE_WINDOW", self.close_win)

    # makes sure that the entire region is scrollable one base_frame is configured
    def config_base(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # draw new original image in tkinter and close the old one
    def draw_orig(self, img: Image):
        self.drawn_orig.close()
        self.drawn_orig = img.copy()
        self.orig_tk = ImageTk.PhotoImage(self.drawn_orig)
        self.orig_label["image"] = self.orig_tk

    # closes the application
    def close_win(self):
        self.running = False
        if self.time_call is not None:
            self.win.after_cancel(self.time_call)
        self.clear_up()
        self.win.destroy()
        self.orig_img.close()
        self.changed_img.close()
        exit(0)

    # draw new changed image in tkinter
    def draw_changed(self, img: Image):
        self.drawn_changed.close()
        self.drawn_changed = img.copy()
        self.changed_tk = ImageTk.PhotoImage(self.drawn_changed)
        self.changed_label["image"] = self.changed_tk

    # when either image is clicked
    def img_clicked(self, event):
        if not self.running:
            return
        if self.start_click is not None: # this is the end point of the rectangle
            x0, y0 = self.start_click
            x1 = event.x
            y1 = event.y
            # make x0, y0 be top left corner and x1, y1 be bottom right
            if x1 < x0:
                x0, x1 = swap(x0, x1)
            if y1 < y0:
                y0, y1 = swap(y0, y1)
            # append to squares drawn to say found difference
            self.squares.append([(x0, y0), (x1, y1)])
            self.start_click = None
            # draw next square on the images
            orig_draw = ImageDraw.Draw(self.square_orig)
            changed_draw = ImageDraw.Draw(self.square_changed)
            orig_draw.rectangle([(x0, y0), (x1, y1)], None, (255, 0, 0))
            changed_draw.rectangle([(x0, y0), (x1, y1)], None, (255, 0, 0))
            self.draw_orig(self.square_orig)
            self.draw_changed(self.square_changed)
        elif self.num_differences <= 0 or (len(self.squares) < self.num_differences):
            self.start_click = (event.x, event.y) # this was the start point

    # mouse is moving across image
    def img_move(self, event):
        if not self.running:
            return
        if self.start_click is not None: # need to draw box the user is selecting
            x0, y0 = self.start_click
            x1 = event.x
            y1 = event.y
            if x1 < x0:
                x0, x1 = swap(x0, x1)
            if y1 < y0:
                y0, y1 = swap(y0, y1)
            # draw the rectangle user would select if clicking
            cur_orig = self.square_orig.copy()
            cur_changed = self.square_changed.copy()
            orig_draw = ImageDraw.Draw(cur_orig)
            changed_draw = ImageDraw.Draw(cur_changed)
            orig_draw.rectangle([(x0, y0), (x1, y1)], None, (255, 0, 0))
            changed_draw.rectangle([(x0, y0), (x1, y1)], None, (255, 0, 0))
            self.draw_orig(cur_orig)
            self.draw_changed(cur_changed)

    # display score and stop timer
    def end_game(self):
        if self.time_call is not None:
            self.win.after_cancel(self.time_call)
        if self.time > 0:
            self.time_label.config(text=f"{sec_to_time(self.time)}")
        else:
            self.time_label.config(text="Time's Up!")
        if self.num_differences > 0:
            self.diff_sol_label.grid_forget()
        self.score = do_score(self.squares, self.solutions, self.time)
        self.diff_sol_label["text"] = f"Score: {self.score}"
        self.diff_sol_label["fg"] = "yellow"
        self.diff_sol_label.grid(row=2, column=1)
        self.running = False

    # countdown timer
    def count_down(self):
        self.time -= 1
        if self.time > 0: # while still running
            self.time_label.config(text=f"{sec_to_time(self.time)}")
            self.time_call = self.win.after(1000, self.count_down)
        else:
            # draw square images
            self.orig_tk = ImageTk.PhotoImage(self.square_orig)
            self.changed_tk = ImageTk.PhotoImage(self.square_changed)
            self.orig_label["image"] = self.orig_tk
            self.changed_label["image"] = self.changed_tk
            self.time_call = None
            self.end_game()

    # listen for u key or escape key for undo feature
    def key_pressed(self, event):
        if ((event.keysym == "Escape" or event.char == 'u') and (len(self.squares) > 0 or self.start_click is not None)) and self.running: # make sure have square to undo and the timer hasn't run out
            if self.start_click is None:
                # remove square from quieue
                self.squares.pop(-1)
                # redraw all the rectangles
                cur_orig = self.orig_img.copy()
                cur_changed = self.changed_img.copy()
                orig_draw = ImageDraw.Draw(cur_orig)
                changed_draw = ImageDraw.Draw(cur_changed)
                for square in self.squares:
                    orig_draw.rectangle(square, None, (255, 0, 0))
                    changed_draw.rectangle(square, None, (255, 0, 0))
                self.square_orig = cur_orig
                self.square_changed = cur_changed
                self.draw_orig(cur_orig)
                self.draw_changed(cur_changed)
            else: # if have start point simply cancel the selecting process
                self.start_click = None
                self.draw_orig(self.square_orig)
                self.draw_changed(self.square_changed)

    # garbage collection
    def clear_up(self):
        self.square_orig.close()
        self.square_changed.close()
        self.drawn_orig.close()
        self.drawn_changed.close()

    # next button pressed -> go onto next stage
    def next_clicked(self):
        if self.running:
            self.end_game()
        else:
            self.clear_up()
            common.release_win(self.win)
            self.win.unbind("<Key>")
            self.win.bind("WM_CLOSE_WINDOW", common.close_win)

    # run main window
    def run(self):
        self.running = True
        self.count_down()
        self.win.mainloop()

# AI window for how our algorithm accomplishes it
class AIWin:
    def __init__(self, win, orig_img: Image, changed_img: Image, num_differences: int, solutions, scroll = False, human_colour = False, sensitivity: int = 20, smallest_img: int = 30):
        self.win = win
        self.win.title("Spot The Difference")

        # have copies as going to draw on them
        self.orig_img = orig_img.copy()
        self.changed_img = changed_img.copy()

        self.human_colour = human_colour
        # sensitivity is used to control how different the pixels must be to be considered different
        if human_colour:
            self.r_sens = sensitivity * RedInvMul
            self.g_sens = sensitivity * GreenInvMul
            self.b_sens = sensitivity * BlueInvMul
        else:
            self.sensitivity = sensitivity

        # smallest img is used to discard objects of few pixels but have high variation
        self.smallest_img = smallest_img
        self.diff_img = self.get_img_diff()
        pixel_objects = []
        self.amp_img = self.get_amp_img_diff()
        
        # find all objects in the image
        pixel_objects = self.find_objects()
        self.objects = []
        for pixel_obj in pixel_objects:
            w0 = self.diff_img.width
            h0 = self.diff_img.height
            w1 = 0
            h1 = 0
            pixel_score = 0
            for pixel in pixel_obj: # finding the bounding rectangles for the objects
                w, h, score = pixel
                if w < w0:
                    w0 = w
                if w > w1:
                    w1 = w
                if h < h0:
                    h0 = h
                if h > h1:
                    h1 = h
                pixel_score += score
            # use average in case have two large objects with a slight change in colour (JPEG compression)
            self.objects.append([(w0, h0), (w1, h1), pixel_score / len(pixel_obj)])
        self.objects.sort(key=itemgetter(2), reverse=True)
        if num_differences > 0 and num_differences <= len(self.objects):
            self.objects = self.objects[0:num_differences]

        self.selections = []

        # draw the bounding rectangles on the images
        orig_draw = ImageDraw.Draw(self.orig_img)
        changed_draw = ImageDraw.Draw(self.changed_img)
        diff_draw = ImageDraw.Draw(self.diff_img)
        amp_draw = ImageDraw.Draw(self.amp_img)
        for obj in self.objects:
            orig_draw.rectangle([obj[0], obj[1]], None, (255, 0, 0))
            changed_draw.rectangle([obj[0], obj[1]], None, (255, 0, 0))
            diff_draw.rectangle([obj[0], obj[1]], None, (255, 0, 0))
            amp_draw.rectangle([obj[0], obj[1]], None, (255, 0, 0))
            self.selections.append([obj[0], obj[1]])
        self.score = do_score(self.selections, solutions, 0) # we won't give algorithm time credit

        # transform to Tk images
        self.orig_tk = ImageTk.PhotoImage(self.orig_img)
        self.changed_tk = ImageTk.PhotoImage(self.changed_img)
        self.diff_tk = ImageTk.PhotoImage(self.diff_img)
        self.amp_tk = ImageTk.PhotoImage(self.amp_img)

        self.canvas = tk.Canvas(self.win, bg="black", borderwidth=0, highlightthickness=0)
        self.base_frame = tk.Frame(self.canvas, bg="black")
        self.image_frame = tk.Frame(self.base_frame, bg="black")
        self.canvas.create_window((0, 0), window=self.base_frame, anchor="nw", width=self.win.winfo_width())
        self.canvas.pack(side="left", fill="both", expand=True)

        # drawing the window
        self.logo_label = tk.Label(self.base_frame, image=common.logo, bg="black")
        self.logo_label.pack(padx=10, pady=10, anchor="nw", side="left")

        self.bar = tk.Frame(self.image_frame, bg="black")
        self.bar.grid(row=1, column=0, columnspan=3)

        self.orig_label = tk.Label(self.bar, image=self.orig_tk, bg="black")
        self.orig_label.grid(row=0, column=0, padx=20, pady=20)


        self.changed_label = tk.Label(self.bar, image=self.changed_tk, bg="black")
        self.changed_label.grid(row=0, column=1, padx=20, pady=20)

        self.diff_label = tk.Label(self.bar, image=self.diff_tk, bg="white")
        self.diff_label.grid(row=1, column=0, padx=20, pady=20)

        self.amp_label = tk.Label(self.bar, image=self.amp_tk, bg="white")
        self.amp_label.grid(row=1, column=1, padx=20, pady=20)

        self.ai_msg = tk.Label(self.image_frame, text="This is what our algorithm did", font=("arial", 30), fg="white", bg="black")
        self.ai_msg.grid(row=0, column=1)

        self.next_button = tk.Button(self.base_frame, image=common.next_img, borderwidth=0, highlightthickness=0, fg="white", bg="black", activebackground="black", activeforeground="white", command=self.next_clicked)
        self.next_button.pack(padx=10, pady=30, anchor="ne", side="right")

        self.score_label = tk.Label(self.image_frame, text=f"Algorithm score: {self.score}", font=("arial", 30), fg="yellow", bg="black")
        self.score_label.grid(row=2, column=1)
        
        self.image_frame.pack(anchor="center")
        
        self.scroll = scroll
        if scroll:
            self.scroll_bar = tk.Scrollbar(self.win, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scroll_bar.set)
            self.scroll_bar.pack(side="right", fill="y")



        self.base_frame.bind("<Configure>", self.config_base)
        self.win.protocol("WM_DELETE_WINDOW", self.close_win)

    # make sure entire base_frame can be scrolled to
    def config_base(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # computes the difference in the pixels of the two images
    def get_img_diff(self):
        data0 = self.orig_img.load()
        data1 = self.changed_img.load()
        img_res = Image.new("RGBA", (self.orig_img.width, self.orig_img.height))
        res_draw = ImageDraw.Draw(img_res)
        for w in range(self.orig_img.width):
            for h in range(self.orig_img.height):
                r0, g0, b0, _ = data0[w, h]
                r1, g1, b1, _ = data1[w, h]
                res_draw.point([(w, h)], (abs(r1 - r0), abs(g1 - g0), abs(b1 - b0), 255))
        return img_res

    # checks the colour is above the threshold and the pixel should be counted as a difference
    def check_colour(self, r, g, b):
        return (not self.human_colour and (r > self.sensitivity or g > self.sensitivity or b > self.sensitivity)) or (self.human_colour and (r > self.r_sens or g > self.g_sens or b > self.b_sens))

    # scores the pixel based on how different it is
    def score_pixel(self, r, g, b):
        if self.human_colour:
            return r * RedMul + g * GreenMul + b * BlueMul
        else:
            return r + g + b
    
    # takes the difference image and has white pixel where a colour channel is about the sensitivity level or else sets it to black. This image is what the algorithm uses for collecting all the objects and drawing boxes around them
    def get_amp_img_diff(self):
        data = self.diff_img.load()
        img_res = Image.new("RGBA", (self.diff_img.width, self.diff_img.height))
        res_draw = ImageDraw.Draw(img_res)
        for w in range(self.diff_img.width):
            for h in range(self.diff_img.height):
                r, g, b, _ = data[w, h]
                if self.check_colour(r, g, b):
                    res_draw.point([w, h], (255, 255, 255, 255))
                else:
                    res_draw.point([w, h], (0, 0, 0, 255))
        return img_res


    # checks if a given pixel should be added and if so does
    def check_pixel(self, obj, img_data, w, h, found, check_pixels):
        r, g, b, _ = img_data[w, h]
        if self.check_colour(r, g, b) and (w, h) not in found:
            found[(w, h)] = True
            obj.append((w, h, self.score_pixel(r, g, b))) # final part is a pixel score which is used if we have too many objects
            check_pixels.append((w, h))

    # look for one pixel that isn't black and then look for all its neighbours and declare an object
    def find_objects(self):
        data = self.diff_img.load()
        found = {} # all the pixels which have been found and shouldn't be used for searching for an object
        res = []
        for w in range(self.diff_img.width):
            for h in range(self.diff_img.height):
                r, g, b, _ = data[w, h]
                # found an object
                if self.check_colour(r, g, b) and (w, h) not in found:
                    found[(w, h)] = True # add to found pixels
                    res.append([(w, h, self.score_pixel(r, g, b))])
                    obj = res[len(res) - 1]
                    check_pixels = []
                    check_pixels.append((w, h))
                    # find all neghbours of object
                    while len(check_pixels) > 0:
                        check_w, check_h = check_pixels.pop(0)
                        if check_w > 0:
                            if check_h > 0:
                                self.check_pixel(obj, data, check_w - 1, check_h - 1, found, check_pixels)
                            if check_h < self.diff_img.height - 1:
                                self.check_pixel(obj, data, check_w - 1, check_h + 1, found, check_pixels)
                            self.check_pixel(obj, data, check_w - 1, check_h, found, check_pixels)
                        if check_w < self.diff_img.width - 1:
                            if check_h > 0:
                                self.check_pixel(obj, data, check_w + 1, check_h - 1, found, check_pixels)
                            if check_h < self.diff_img.height - 1:
                                self.check_pixel(obj, data, check_w + 1, check_h + 1, found, check_pixels)
                            self.check_pixel(obj, data, check_w + 1, check_h, found, check_pixels)
                        if check_h > 0:
                            self.check_pixel(obj, data, check_w, check_h - 1, found, check_pixels)
                        if check_h < self.diff_img.height - 1:
                            self.check_pixel(obj, data, check_w, check_h + 1, found, check_pixels)
        num_rem = 0
        for i in range(len(res)):
            if len(res[i - num_rem]) < self.smallest_img:
                res.pop(i - num_rem)
                num_rem += 1
        return res

    # close the window and exit the application
    def close_win(self):
        self.clear_up()
        self.win.destroy()
        exit(0)

    # garbage collection
    def clear_up(self):
        self.orig_img.close()
        self.changed_img.close()
        self.diff_img.close()
        self.amp_img.close()

    # for going onto what's after this window
    def next_clicked(self):
        self.clear_up()
        common.release_win(self.win)
        # no more key events for window
        self.win.unbind("<Key>")
        self.win.bind("WM_CLOSE_WINDOW", common.close_win)

    # we don't have much to do in run
    def run(self):
        self.win.mainloop()

# an object to hold all the data about the two images to find the differences between
class ImageDiff:
    def __init__(self):
        self.name = None
        self.orig_name = None
        self.diff_name = None
        self.orig_img = None
        self.diff_img = None
        self.differences = None
        self.solutions = None

    def __str__(self):
        return f"{{Name: {self.name}, orig img: {self.orig_name}, diff img: {self.diff_name}, num differences: {self.differences}, solutions: {self.solutions}}}"



def run(win):
    # load image data from config file
    config_file = open("config.json", "r")
    config_text = read_all(config_file)
    config_file.close()

    config_text = config_text.strip()
    # parse json data
    config_data = json.loads(config_text)

    images = []

    # extract the specific image data from the json file
    for item in config_data:
        image_obj = ImageDiff()
        image_obj.name = item
        image_json_data = config_data[item]
        image_obj.orig_name = image_json_data["before"]
        image_obj.diff_name = image_json_data["after"]
        image_obj.differences = image_json_data["num_differences"]
        solutions_json = image_json_data["solutions"]
        solutions = []
        for sol_json in solutions_json:
            s = Solution()
            s.sol = [(sol_json["top_left"]["w"], sol_json["top_left"]["h"]), (sol_json["bottom_right"]["w"], sol_json["bottom_right"]["h"])]
            s.score = sol_json["score"]
            if "alt" in sol_json:
                alt_sol_json = sol_json["alt"]
                s.alt = [(alt_sol_json["top_left"]["w"], alt_sol_json["top_left"]["h"]), (alt_sol_json["bottom_right"]["w"], alt_sol_json["bottom_right"]["h"])]
            solutions.append(s)
        image_obj.solutions = solutions
        images.append(image_obj)

    # choose random image to use
    sel_img = random.choice(images)

    # Open the images
    sel_img.orig_img = Image.open(sel_img.orig_name).convert("RGBA")
    sel_img.diff_img = Image.open(sel_img.diff_name).convert("RGBA")

    # run main program
    user_win = UserWin(win, sel_img.orig_img, sel_img.diff_img, sel_img.differences, sel_img.solutions)
    user_win.run()
    score = user_win.score
    ai_win = AIWin(win, sel_img.orig_img, sel_img.diff_img, sel_img.differences, sel_img.solutions, scroll=True)
    ai_win.run()
    sel_img.orig_img.close()
    sel_img.diff_img.close()
    return (user_win.score, user_win.time)
