
# dependecies: Pillow (Python module)
from PIL import Image, ImageDraw

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

res = get_img_diff(orig, changed)

# close input images
orig.close()
changed.close()

# show the image and close
res.show()
res.close()
