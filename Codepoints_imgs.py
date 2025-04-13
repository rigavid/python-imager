from pyimager import *

usage_colors = {
    "control": COL.red,
    "format": COL.blue,
    "diac ab": COL.greenYellow,
    "diac bl": COL.yellowGreen,
    "in diac": COL.darkGreen,
    "symbols": COL.pink,
    "LATIN": COL.darkBlue,
    "latin": COL.lightBlue,
    "CYRILIC": COL.darkGreen,
    "cyrilic": COL.lightGreen,
    "VIET": COL.darkSalmon,
    "viet": COL.salmon,
    "GREEK": COL.darkRed,
    "greek": COL.orangeRed,
    "A.GREEK": COL.darkMagenta,
    "a.greek": COL.magenta,
    "o.greek": COL.aqua,
    "hebrew": COL.olive,
    "mkhedruli": COL.yellow,
    "hiragana": COL.red,
    "katakana": COL.blue,
    "ARMENIAN": COL.darkOrange,
    "armenian": COL.orange,
    "si po of": COL.khaki,
    "si po co": COL.brown,
    "si po ra": COL.maroon,
    "si po al": COL.black}

try:
    with open("./CODEPOINTS.md", "r", encoding="utf8") as file:
        text = file.read()
    table = text.split("##")[2]
    lines = table.split("\n")[3::]
    data = []
    for l in lines:
        l = [i.strip(" ") for i in l.split("|") if i != ""]
        if l == []: continue
        plage = l[0].split("-")
        if len(plage) == 1: plage *= 2
        data.append((*plage, l[-1]))
    try: os.mkdir("./imgs")
    except: pass
except:
    print("Error opening file")
    raise SystemExit

print(data)

chars = data
size = 1000
D = size//10; dists = [i for i in range(0, size+1, D)]

ALP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

if True:
    img_00_99 = new_img(dimensions=[size, size])
    for d, f, c in chars:
        if d.isdecimal():
            for i in range(int(d), int(f)+1):
                i = f"{i:0>2}"; x, y = int(i[1]), int(i[0])
                img_00_99.rectangle([dists[x], dists[y]], [dists[x]+D, dists[y]+D], COL.new(usage_colors[c]), 0, 2)
                img_00_99.write(c[0], [dists[x]+D/3, dists[y]+D/3*2], COL.green, D//50, D/50, lineType=2)
    for n, i in enumerate(range(0, size+1, D)):
        img_00_99.line([0, i], [size, i], COL.gray, 2 if n%2==0 else 1, 2)
        img_00_99.line([i, 0], [i, size], COL.gray, 1, 2)
    img_00_99.save_img("./imgs", "00-99.jpg")

if True:
    D = size//10; dists = [i for i in range(0, size+1, D)]
    img_A0_Z9 = new_img(dimensions=[size, size/10*26])
    for d, f, c in chars:
        if not d.isdecimal() and len(d) == 2:
            y1, y2 = ALP.index(d[0]), ALP.index(f[0])
            for y in range(y1, y2+1):
                x1, x2 = 0 if y>y1 else int(d[1]), 9 if y<y2 else int(f[1])
                for x in range(x1, x2+1):
                    img_A0_Z9.rectangle([dists[x], dists[y]], [dists[x]+D, dists[y]+D], COL.new(usage_colors[c]), 0, 2)
                    img_A0_Z9.write(c[0], [dists[x]+D/3, dists[y]+D/3*2], COL.green, D//50, D/50, lineType=2)
    for i in range(26):
        img_A0_Z9.line([0, D*i], [size, D*i], COL.gray, 2 if i%5==0 else 1, 2)
        img_A0_Z9.line([D*i, 0], [D*i, size/10*26], COL.gray, 2 if i%5==0 else 1, 2)
    img_A0_Z9.save_img("./imgs", "A0-Z9.jpg")

if True:
    D = size//100; dists = [i for i in range(0, size+1, D)]
    img_A00_Z99 = new_img(dimensions=[size, size/100*26])
    for d, f, c in chars:
        if not d.isdecimal() and len(d) == 3:
            y1, y2 = ALP.index(d[0]), ALP.index(f[0])
            for y in range(y1, y2+1):
                x1, x2 = 0 if y>y1 else int(d[1::]), 99 if y<y2 else int(f[1::])
                for x in range(x1, x2+1):
                    img_A00_Z99.rectangle([dists[x], dists[y]], [dists[x]+D, dists[y]+D], COL.new(usage_colors[c]), 0)
    for i in range(260):
        img_A00_Z99.line([0, D*i], [size, D*i], COL.gray, 1)
        img_A00_Z99.line([D*i, 0], [D*i, size/100*26], COL.gray, 2 if i%10 == 0 else 1)
    img_A00_Z99.save_img("./imgs", "A00-Z99.jpg")