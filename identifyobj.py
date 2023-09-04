from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw
from operator import itemgetter
import json
import random

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

  I would like to write my formal complaint against the sun which tried to blind me as I was writing my code
  Please don't comment on how I have basically treated squares and rectangles as the same shape
  I hope my commit with no changes isn't noticed
"""

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

# calculates the score for the player leniance -> how far either side of axis error can be to still be rewarded points for solution. Score algorithm may change in future
def do_score(selections, solutions, time, leniance = 5):
    num_correct = 0 # how many of the solutions the player got right
    score = 0
    solutions_used = []
    for rec in selections:
        rec_solutions = []
        for i in range(len(solutions)):
            if i not in solutions_used:
                sol = solutions[i]
                x0, y0 = sol[0]
                x1, y1 = sol[1]
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
                    rec_solutions.append(i) # possible solution
        # select lowest scoring solution
        chosen = -1
        chosen_score = 1000000000 # don't add scores bigger than this
        for sol_index in rec_solutions:
            if solutions[sol_index][2] < chosen_score:
                chosen = sol_index
                chosen_score = solutions[sol_index][2]
        if chosen != -1:
            num_correct += 1
            solutions_used.append(chosen)
            score += solutions[sol_index][2]
    if num_correct == len(solutions):
        score += time # time bonus for if have all solutions and there is time left
    return score
# solutions should be in the format [top_left_pixel, bottom_right_pixel, score] where score is the points for finding that difference

# User Window for player's attempt
class UserWin:
    def __init__(self, win, orig_img: Image, changed_img: Image, num_differences: int, solutions):
        # creates Tkinter window, sets background and creates array of squares drawn and where the first click was
        self.win = win
        self.win.title("Spot The Difference")
        self.win["bg"] = "black"
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

        self.time = 60 # time to run for
        self.score = 0 # the player's score
        self.running = True # timer hasn't run out
        self.num_differences = num_differences # how many differences to look for (0 or less will turn off differences display)
        self.lower_bar = Frame(self.win, bg="black")
        self.lower_bar.grid(row=1, column=0, columnspan=3)

        # displaying things on the screen
        self.time_label = Label(self.win, text=f"{sec_to_time(self.time)}", font=("arial", 30), bg="black", fg="white")
        self.time_label.grid(row=0, column=1)

        self.diff_sol_label = Label(self.win, text=f"", font=("arial", 30), bg="black", fg="magenta")

        if num_differences > 0:
            self.diff_sol_label["text"] = f"Differences: {num_differences}"
            self.diff_sol_label.grid(row=2, column=1)

        self.next_button = Button(self.win, text="Next", font=("arial", 30), bg="black", fg="white", command=self.next_clicked)
        self.next_button.grid(row=0, column=2, sticky="ne")

        # where the images are
        self.orig_label = Label(self.lower_bar, image=self.orig_tk, bg="black")
        self.orig_label.grid(row=0, column=0, padx=20, pady=20)

        self.changed_label = Label(self.lower_bar, image=self.changed_tk, bg="black")
        self.changed_label.grid(row=0, column=1, padx=20, pady=20)

        # events for images and the window
        self.orig_label.bind("<Button-1>", self.img_clicked)
        self.orig_label.bind("<Motion>", self.img_move)
        self.changed_label.bind("<Button-1>", self.img_clicked)
        self.changed_label.bind("<Motion>", self.img_move)
        self.win.bind("<Key>", self.key_pressed)
        self.win.protocol("WM_DELETE_WINDOW", self.close_win)

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
        self.time_label.config(text=f"{sec_to_time(self.time)}")
        if self.num_differences > 0:
            self.diff_sol_label.grid_forget()
        self.score = do_score(self.squares, self.solutions, self.time)
        self.diff_sol_label["text"] = f"Score: {self.score}"
        self.diff_sol_label["fg"] = "yellow"
        self.diff_sol_label.grid(row=2, column=1)
        self.running = False

    # countdown timer
    def count_down(self):
        self.time_label.config(text=f"{sec_to_time(self.time)}")
        if self.time > 0: # while still running
            self.time -= 1
            self.time_call = self.win.after(1000, self.count_down)
        else:
            self.time_label.config(text="Time's Up!")
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
            self.win.quit()
            self.changed_label.destroy()
            self.orig_label.destroy()
            self.lower_bar.destroy()
            self.next_button.destroy()
            self.time_label.destroy()
            self.diff_sol_label.destroy()

    # run main window
    def run(self):
        self.running = True
        self.count_down()
        self.win.mainloop()

# AI window for how our algorithm accomplishes it
class AIWin:
    def __init__(self, win, orig_img: Image, changed_img: Image, num_differences: int, solutions, sensitivity: int = 20, smallest_img: int = 10):
        self.win = win
        self.win.title("Spot The Difference")

        # have copies as going to draw on them
        self.orig_img = orig_img.copy()
        self.changed_img = changed_img.copy()

        # sensitivity is used to control how different the pixels must be to be considered different
        self.sensitivity = sensitivity
        # smallest img is used to discard objects of few pixels but have high variation
        self.smallest_img = smallest_img
        self.diff_img = self.get_img_diff()
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

        # drawing the window
        self.bar = Frame(self.win, bg="black")
        self.bar.grid(row=1, column=0, columnspan=3)

        self.orig_label = Label(self.bar, image=self.orig_tk, bg="black")
        self.orig_label.grid(row=0, column=0, padx=20, pady=20)


        self.changed_label = Label(self.bar, image=self.changed_tk, bg="black")
        self.changed_label.grid(row=0, column=1, padx=20, pady=20)

        self.diff_label = Label(self.bar, image=self.diff_tk, bg="white")
        self.diff_label.grid(row=1, column=0, padx=20, pady=20)

        self.amp_label = Label(self.bar, image=self.amp_tk, bg="white")
        self.amp_label.grid(row=1, column=1, padx=20, pady=20)

        self.ai_msg = Label(self.win, text="This is what our algorithm did", font=("arial", 30), fg="white", bg="black")
        self.ai_msg.grid(row=0, column=1)

        self.next_button = Button(self.win, text="Next", font=("arial", 30), fg="white", bg="black", command=self.next_clicked)
        self.next_button.grid(row=0, column=2, sticky="ne")

        self.score_label = Label(self.win, text=f"Algorithm score: {self.score}", font=("arial", 30), fg="yellow", bg="black")
        self.score_label.grid(row=2, column=1)

        self.win.protocol("WM_DELETE_WINDOW", self.close_win)

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

    # takes the difference image and has white pixel where a colour channel is about the sensitivity level or else sets it to black. This image is what the algorithm uses for collecting all the objects and drawing boxes around them
    def get_amp_img_diff(self):
        data = self.diff_img.load()
        img_res = Image.new("RGBA", (self.diff_img.width, self.diff_img.height))
        res_draw = ImageDraw.Draw(img_res)
        for w in range(self.diff_img.width):
            for h in range(self.diff_img.height):
                r, g, b, _ = data[w, h]
                if r > self.sensitivity or g > self.sensitivity or b > self.sensitivity:
                    res_draw.point([w, h], (255, 255, 255, 255))
                else:
                    res_draw.point([w, h], (0, 0, 0, 255))
        return img_res

    # checks if a given pixel should be added and if so does
    def check_pixel(self, obj, img_data, w, h, found, check_pixels):
        r, g, b, _ = img_data[w, h]
        if (r > self.sensitivity or g > self.sensitivity or b > self.sensitivity) and (w, h) not in found:
            found[(w, h)] = True
            obj.append((w, h, r + g + b)) # final part is a pixel score which is used if we have too many objects
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
                if (r > self.sensitivity or g > self.sensitivity or b > self.sensitivity) and (w, h) not in found:
                    found[(w, h)] = True # add to found pixels
                    res.append([(w, h, r + g + b)])
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
        self.win.quit()
        self.ai_msg.destroy()
        self.next_button.destroy()
        self.orig_label.destroy()
        self.changed_label.destroy()
        self.diff_label.destroy()
        self.amp_label.destroy()
        self.bar.destroy()
        self.score_label.destroy()

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
        solutions.append([(sol_json["top_left"]["w"], sol_json["top_left"]["h"]), (sol_json["bottom_right"]["w"], sol_json["bottom_right"]["h"]), sol_json["score"]])
    image_obj.solutions = solutions
    images.append(image_obj)

# choose random image to use
sel_img = random.choice(images)

# Open the images
sel_img.orig_img = Image.open(sel_img.orig_name).convert("RGBA")
sel_img.diff_img = Image.open(sel_img.diff_name).convert("RGBA")

# setup window
win = Tk()
win["bg"] = "black"

logo = Image.open("Logo_Dark.png")
logo_tk = ImageTk.PhotoImage(logo)
logo_label = Label(win, image=logo_tk, bg="black")
logo_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

# run main program
user_win = UserWin(win, sel_img.orig_img, sel_img.diff_img, sel_img.differences, sel_img.solutions)
user_win.run()
score = user_win.score
ai_win = AIWin(win, sel_img.orig_img, sel_img.diff_img, sel_img.differences, sel_img.solutions)
ai_win.run()
win.destroy()
sel_img.orig_img.close()
sel_img.diff_img.close()
logo.close()
print(f"score: {score}")
