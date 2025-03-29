import pyimager as pyi

test_letters = ""
n = 3
for l in ("A", "B"):
    for i in range(10):
        for j in range(10):
            test_letters += f"^{l}{i}{j}^"
        if int(f"{i}{j}")<99 or l=="A": test_letters += "\n" if l == "A" else "\n"+"\t"*n
    if l == "A": test_letters += "\b\r"+"\t"*n
test_symbols = ""
for n in range(10):
    for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        test_symbols += f"^{l}{n}^"
    test_symbols += "\n"

strs = [
    test_letters, test_symbols,
    "ÀÁÂÄǍÅĂȀA̋ȦĀÃA̍A̎\nàáâäǎåăȁa̋ȧāãa̍a̎",
    "Dès Noël, où un zéphyr haï me vêt de\nglaçons würmiens, je dîne d’exquis\nrôtis de bœuf au kir, à l’aÿ\nd’âge mûr, &cætera.",
    "Ξεσκεπάζω τὴν ψυχοφθόρα βδελυγμία.",
    "いろはにほへと ちりぬるを わかよたれそ つねならむ\nうゐのおくやま けふこえて あさきゆめみし ゑひもせす",
    "Съешь ещё этих мягких французских\nбулок, да выпей же чаю.",
    "Nechť již hříšné saxofony ďáblů\nrozzvučí síň úděsnými tóny waltzu,\ntanga a quickstepu.",
    "Tất cả mọi người sinh ra đều\nđược tự do và bình đẳng về\nnhân phẩm và quyền lợi.",
    "Kæmi ný öxi hér ykist þjófum\nnú bæði víl og ádrepa.",
    "דג סקרן שט בים מאוכזב ולפתע מצא חברה",
    "^21^UL^21^\t^22^TL^22^\t^23^OL^23^\t^24^IT^24^\t^25^BD^25^\t^26^CI^26^\t^27^TN^27^\t^28^VM^28^\t^29^HM^29^\n^21^^22^U^23^T^23^L^21^^22^\n\n",
    "^BG:ffffff^BG:ffffff^BG:ffffff^\n^FG:ffffff^FG:ffffff^FG:ffffff^\n^21^^LS:ffffff^UL:LS:ffffff^LS:ffffff^^21^"
]

import unicodedata


def update(img, help=False, a=0, ind=0, m=False):
    i:pyi.image = pyi.new_img(background=pyi.COL.black)
    i.text(strs[ind%len(strs)], [i/2 for i in pyi.RES.resolution], fontSize=10, lineType=2, thickness=2, help=help, angle=a, monospace=m)
    img.img = i.img
    img.line([0, pyi.RES.resolution[1]/2], [pyi.RES.resolution[0], pyi.RES.resolution[1]/2], pyi.COL.green, 1, 2)
    img.line([pyi.RES.resolution[0]/2, 0], [pyi.RES.resolution[0]/2, pyi.RES.resolution[1]], pyi.COL.green, 1, 2)
    img.circle([i/2 for i in pyi.RES.resolution], 4, pyi.COL.purple, 0, 2)

def main():
    img, help, a, i = pyi.new_img(background=pyi.COL.black, name="Text test!").build(), False, 0, 0
    img.fullscreen = True
    m = False
    while img.is_opened():
        update(img, help, a, i, m)
        wk = img.show_()
        if wk == 8: help = not help
        if wk == ord("r"): a += 30
        if wk == ord("c"): i += 1
        if wk == ord("x"): i -= 1
        if wk == ord("h"): print(pyi.Text(strs[i]).text.__chain__str__())
        if wk == ord("m"): m = not m

if __name__ == "__main__":
    pyi.COL.help = pyi.COL.blue
    main()