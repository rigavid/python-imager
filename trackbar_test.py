from pyimager.main import *

img = new_img(name="Testing trackbars")
fs, tk = 100, 3

def p(event, x, y, flags, params):
    if event==cv2.EVENT_LBUTTONDOWN:
        print(f"Value: {params[0].get()}")

t = img.trackbar("TEST", min=10, fontSize=fs, thickness=tk)
b = img.button("Test", fontSize=fs, thickness=tk); b.on_click(p, [t])

s = 100
img.textSize("A", fontSize=s)
img.text("A", ct, fontSize=s)

img.build()
while img.is_opened():
    wk = img.show()
    if wk == -1: pass