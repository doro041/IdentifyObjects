from tkinter import *
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw

"""
Sources I (Fraser) have used (other than documentation)  I don't know Tkinter - Fraser
  https://www.geeksforgeeks.org/loading-images-in-tkinter-using-pil/ for using Pillow with Tkinter
  https://pythonguides.com/tkinter/ this also for working with Tkinter
  https://tkinterexamples.com/events/mouse/ for mouse events

  I think https://stackoverflow.com/questions/47852221/tkinter-after-method-executing-immediately for sorting out my timer. I originally thought I wasn't calling it as a function but I now think I was.

  I would like to write my formal complaint against the sun which tried to blind me as I was writing my code
  Please don't comment on how I have basically treated squares and rectangles as the same shape
  I hope my commit with no changes isn't noticed
"""


# converts seconds to str format in time in the format 0:00
def sec_to_time(time: int):
    if time > 599 or time < 0:
        return "?:??"
    return str(time // 60) + ":" + format(time % 60, "0=2")

# swaps a and b and returns as tuple
def swap(a, b):
    return (b, a)

class UserWin:
    def __init__(self, orig_img: Image, changed_img: Image, fin_callback):
        # creates Tkinter window, sets background and creates array of squares drawn and where the first click was
        self.win = Tk()
        self.win.title("Spot The Difference")
        self.win["bg"] = "black"
        self.squares = []
        self.start_click = None

        # load logo and set images for user to draw to
        self.logo = ImageTk.PhotoImage(Image.open("Logo_Dark.png"))
        self.orig_img = orig_img # the original images
        self.changed_img = changed_img
        self.orig_tk = ImageTk.PhotoImage(orig_img) # in format for Tk to render -> these will hold the currently drawn images but are redundant
        self.changed_tk = ImageTk.PhotoImage(changed_img)
        self.square_orig = orig_img.copy() # original image with all the selected squares drawn on it (used so have less drawing to do when user draws squares)
        self.square_changed = changed_img.copy()

        self.time = 60 # time to run for
        self.running = True # timer hasn't run out
        self.lower_bar = Frame(self.win, bg="black")
        self.lower_bar.grid(row=1, column=0, columnspan=3)

        # displaying things on the screen
        self.time_label = Label(self.win, text=f"{sec_to_time(self.time)}", font=("arial", 30), bg="black", fg="white")
        self.time_label.grid(row=0, column=1)

        self.next_button = Button(self.win, text="Next", font=("arial", 30), bg="black", fg="white")
        self.next_button.grid(row=0, column=2, sticky="ne")

        self.logo_label = Label(self.win, image=self.logo, bg="black")
        self.logo_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        # where the images are
        self.orig_label = Label(self.lower_bar, image=self.orig_tk, bg="black")
        self.orig_label.grid(row=1, column=0, padx=20, pady=20)

        self.changed_label = Label(self.lower_bar, image=self.changed_tk, bg="black")
        self.changed_label.grid(row=1, column=1, padx=20, pady=20)

        # events for images and the window
        self.next_button.bind("<Button>", self.next_clicked)
        self.orig_label.bind("<Button-1>", self.img_clicked)
        self.orig_label.bind("<Motion>", self.img_move)
        self.changed_label.bind("<Button-1>", self.img_clicked)
        self.changed_label.bind("<Motion>", self.img_move)
        self.win.bind("<Key>", self.key_pressed)

        # what should be called when time has run out
        self.fin_callback = fin_callback

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
            self.orig_tk = ImageTk.PhotoImage(self.square_orig)
            self.changed_tk = ImageTk.PhotoImage(self.square_changed)
            self.orig_label["image"] = self.orig_tk
            self.changed_label["image"] = self.changed_tk
        else:
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
            self.orig_tk = ImageTk.PhotoImage(cur_orig)
            self.changed_tk = ImageTk.PhotoImage(cur_changed)
            self.orig_label["image"] = self.orig_tk
            self.changed_label["image"] = self.changed_tk


    # countdown timer
    def count_down(self):
        self.time_label.config(text=f"{sec_to_time(self.time)}")
        if self.time > 0: # while still running
            self.time -= 1
            self.win.after(1000, self.count_down)
        else:
            self.time_label.config(text="Time's Up!")
            # draw square images
            self.orig_tk = ImageTk.PhotoImage(self.square_orig)
            self.changed_tk = ImageTk.PhotoImage(self.square_changed)
            self.orig_label["image"] = self.orig_tk
            self.changed_label["image"] = self.changed_tk
            self.running = False # time ran out

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
                self.orig_tk = ImageTk.PhotoImage(cur_orig)
                self.changed_tk = ImageTk.PhotoImage(cur_changed)
                self.orig_label["image"] = self.orig_tk
                self.changed_label["image"] = self.changed_tk
            else: # if have start point simply cancel the selecting process
                self.start_click = None
                self.orig_tk = ImageTk.PhotoImage(self.square_orig)
                self.changed_tk = ImageTk.PhotoImage(self.square_changed)
                self.orig_label["image"] = self.orig_tk
                self.changed_label["image"] = self.changed_tk

    def next_clicked(self, event):
        self.running = False
        self.win.destroy()
        self.fin_callback(self.squares)

    # run main window
    def run(self):
        self.running = True
        self.count_down()
        self.win.mainloop()

Sensitivity = 20


# Should next go onto AI attempt and possibly do something with squares
def fin_callback(squares):
    exit(0)

# Open the images
orig = Image.open("tux_small.png").convert("RGBA")
changed = Image.open("tux_small2.png").convert("RGBA")

user_win = UserWin(orig, changed, fin_callback)

user_win.run()

# computes the difference in the pixels of the two images
def get_img_diff(img0: Image, img1: Image):
    if img0.width != img1.width or img0.height != img1.height:
        return None
    data0 = img0.load()
    data1 = img1.load()
    img_res = Image.new("RGBA", (img0.width, img0.height))
    res_draw = ImageDraw.Draw(img_res)
    for w in range(img0.width):
        for h in range(img0.height):
            r0, g0, b0, _ = data0[w, h]
            r1, g1, b1, _ = data1[w, h]
            res_draw.point([(w, h)], (abs(r1 - r0), abs(g1 - g0), abs(b1 - b0), 255))
    return img_res

# checks if a given pixel should be added and if so does
def check_pixel(obj, img_data, w, h, found, check_pixels):
    r, g, b, _ = img_data[w, h]
    if (r > Sensitivity or g > Sensitivity or b > Sensitivity) and (w, h) not in found:
        found[(w, h)] = True
        obj.append((w, h))
        check_pixels.append((w, h))

# look for one pixel that isn't black and then look for all its neighbours and declare an object
def find_objects(diff_img: Image):
    data = diff_img.load()
    found = {} # all the pixels which have been found and shouldn't be used for searching for an object
    res = []
    for w in range(diff_img.width):
        for h in range(diff_img.height):
            r, g, b, _ = data[w, h]
            # found an object
            if (r > Sensitivity or g > Sensitivity or b > Sensitivity) and (w, h) not in found:
                found[(w, h)] = True # add to found pixels
                res.append([(w, h)])
                obj = res[len(res) - 1]
                check_pixels = []
                check_pixels.append((w, h))
                # find all neghbours of object
                while len(check_pixels) > 0:
                    check_w, check_h = check_pixels.pop(0)
                    if check_w > 0:
                        if check_h > 0:
                            check_pixel(obj, data, check_w - 1, check_h - 1, found, check_pixels)
                        if check_h < diff_img.height - 1:
                            check_pixel(obj, data, check_w - 1, check_h + 1, found, check_pixels)
                        check_pixel(obj, data, check_w - 1, check_h, found, check_pixels)
                    if check_w < diff_img.width - 1:
                        if check_h > 0:
                            check_pixel(obj, data, check_w + 1, check_h - 1, found, check_pixels)
                        if check_h < diff_img.height - 1:
                            check_pixel(obj, data, check_w + 1, check_h + 1, found, check_pixels)
                        check_pixel(obj, data, check_w + 1, check_h, found, check_pixels)
                    if check_h > 0:
                        check_pixel(obj, data, check_w, check_h - 1, found, check_pixels)
                    if check_h < diff_img.height - 1:
                        check_pixel(obj, data, check_w, check_h + 1, found, check_pixels)
    return res



diff_img = get_img_diff(orig, changed)

# close images we don't need anymore
orig.close()

objs = find_objects(diff_img)

diff_img.close()

diff_draw = ImageDraw.Draw(changed)

for obj in objs:
    w1 = 0
    h1 = 0
    w0 = diff_img.width
    h0 = diff_img.height
    for pixel in obj:
        w, h = pixel
        if w < w0:
            w0 = w
        if w > w1:
            w1 = w
        if h < h0:
            h0 = h
        if h > h1:
            h1 = h
    diff_draw.line([(w0, h0), (w1, h0), (w1, h1), (w0, h1), (w0, h0)], (0, 0, 255, 255))

# show the image and close
changed.show()
changed.close()
