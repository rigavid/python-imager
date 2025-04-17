import pyimager as pyi

test_letters = ""
n = 3
for l in "ABCD":
    for i in range(10):
        for j in range(10):
            test_letters += f"^{l}{i}{j}^"
        if int(f"{i}{j}")<99 or l=="A": test_letters += "\n" if l == "A" or l == "C" else "\n"+"\t"*n
    if l == "A" or l == "C": test_letters += "\b\r"+"\t"*n
    if l == "B":
        test_letters_a_b = test_letters
        test_letters = ""
test_letters_c_d = test_letters

test_symbols = ""
for n in range(10):
    for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        test_symbols += f"^{l}{n}^"
    test_symbols += "\n"

strs = [
    test_symbols, test_letters_a_b, test_letters_c_d,
    "ÀÁÂÄǍÅĂȀA̋ȦĀÃA̍A̎^54^A^80^A^62^A^63^A\nàáâäǎåăȁa̋ȧāãa̍a̎^54^a^80^a^62^a^63^a",
    "Dès Noël, où un zéphyr haï me vêt de\nglaçons würmiens, je dîne d’exquis\nrôtis de bœuf au kir, à l’aÿ\nd’âge mûr, &cætera.",
    "Ξεσκεπάζω τὴν ψυχοφθόρα βδελυγμία.",
    "いろはにほへと ちりぬるを わかよたれそ つねならむ\nうゐのおくやま けふこえて あさきゆめみし ゑひもせす",
    "Съешь ещё этих мягких французских\nбулок, да выпей же чаю.",
    "Nechť již hříšné saxofony ďáblů\nrozzvučí síň úděsnými tóny waltzu,\ntanga a quickstepu.",
    "Tất cả mọi người sinh ra đều\nđược tự do và bình đẳng về\nnhân phẩm và quyền lợi.",
    "Kæmi ný öxi hér ykist þjófum\nnú bæði víl og ádrepa.",
    "דג סקרן שט בים מאוכזב ולפתע מצא חברה",
    "^21^UL^21^\t^22^TL^22^\t^23^OL^23^\t^24^IT^24^\t^25^BD^25^\n^26^CI^26^\t^27^TN^27^\t^28^VM^28^\t^29^HM^29^\n^21^^22^U^23^T^23^L^21^^22^",
    "^BG:ffffff^BG:ffffff^BG:ffffff^\n^FG:ffffff^FG:ffffff^FG:ffffff^\n^21^^LS:ffffff^UL:LS:ffffff^LS:ffffff^^21^"
]

def update(img, help=False, a=0, ind=0, m=False, il=0):
    i:pyi.image = pyi.new_img(background=pyi.COL.black)
    i.text(strs[ind%len(strs)], [i/2 for i in pyi.RES.resolution], fontSize=10, lineType=2, thickness=2, help=help, angle=a, monospace=m, interligne=il)
    img.img = i.img
    img.line([0, pyi.RES.resolution[1]/2], [pyi.RES.resolution[0], pyi.RES.resolution[1]/2], pyi.COL.green, 1, 2)
    img.line([pyi.RES.resolution[0]/2, 0], [pyi.RES.resolution[0]/2, pyi.RES.resolution[1]], pyi.COL.green, 1, 2)
    img.circle([i/2 for i in pyi.RES.resolution], 4, pyi.COL.purple, 0, 2)

def main():
    img, help, a, i = pyi.new_img(background=pyi.COL.black, name="Text test!").build(), False, 0, 0
    img.fullscreen = True
    m = False
    il = 0
    while img.is_opened():
        update(img, help, a, i, m, il)
        wk = img.show_()
        if wk == 32: help = not help
        if wk == ord("r"): a += 30
        if wk == ord("c"): i += 1
        if wk == ord("x"): i -= 1
        if wk == ord("h"):
            print(pyi.Text(strs[i]).text.__chain__str__())
            print(img.size())
        if wk == ord("m"): m = not m
        if wk == ord("+"): il += 0.1
        if wk == ord("-"): il -= 0.1

if __name__ == "__main__":
    pyi.COL.help = pyi.COL.blue
    main()