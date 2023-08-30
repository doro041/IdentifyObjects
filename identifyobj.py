
# dependecies: Pillow (Python module)
from PIL import Image, ImageDraw

Sensitivity = 20

# Open the images
orig = Image.open("tux.png").convert("RGBA")
changed = Image.open("tux2.png").convert("RGBA")

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
