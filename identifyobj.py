from PIL import Image, ImageDraw

orig_img = []
changed_img = []
width = 0
height = 0

with Image.open("tux.png").convert("RGBA") as orig:
    orig_data = orig.load()
    width = orig.width
    height = orig.height
    for w in range(orig.width):
        for h in range(orig.height):
            r, g, b, _ = orig_data[w, h]
            orig_img.append((r, g, b))

with Image.open("tux2.png").convert("RGBA") as changed:
    changed_data = changed.load()
    for w in range(changed.width):
        for h in range(changed.height):
            r, g, b, _ = changed_data[w, h]
            changed_img.append((r, g, b))

def get_img_diff(img0, img1):
    img_res = []
    for i in range(len(img0)):
        r_0, g_0, b_0 = img0[i]
        r_1, g_1, b_1 = img1[i]
        img_res.append((abs(r_1 - r_0), abs(g_1 - g_0), abs(b_1 - b_0)))
    return img_res

res = get_img_diff(orig_img, changed_img)
res_img = Image.new("RGBA", (width, height))

draw = ImageDraw.Draw(res_img)
for w in range(width):
    for h in range(height):
        r, g, b = res[w * height + h]
        draw.point([(w, h)], (r, g, b, 255))

res_img.show()
res_img.close()
