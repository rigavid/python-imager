import pyimager as pyi

test_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆŒÞÐ\nАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯĐ\nΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣƩΤΥΦΧΨΩϘϠͲϵ϶\nabcdefghijklmnopqrstuvwxyzæœþð\nабвгдеёжзийклмнопрстуфхцчшщъыьэюяđ\nαβγδεζηθικλμνξοπρσςτυφχψωϙϡͳϑϐ\nאבגדהוזחטיכךלמםנןסעפףצץקרשתבּגּדּכּךּפּףּשׁשׂתּוּוֹ\nაბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"
teste_japonais = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわゐゑをんゃゅ\nアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヰヱヲンャュ"


strs = [test_letters, teste_japonais,
    "ÀÁÂÄǍÅĂȀA̋ȦĀÃA̍A̎\nàáâäǎåăȁa̋ȧāãa̍a̎",
    "Dès Noël, où un zéphyr haï me vêt de\nglaçons würmiens, je dîne d’exquis\nrôtis de bœuf au kir, à l’aÿ\nd’âge mûr, &cætera.",
    "Ξεσκεπάζω τὴν ψυχοφθόρα βδελυγμία.",
    "いろはにほへと ちりぬるを わかよたれそ つねならむ\nうゐのおくやま けふこえて あさきゆめみし ゑひもせす",
    "Съешь ещё этих мягких французских\nбулок, да выпей же чаю.",
    "Nechť již hříšné saxofony ďáblů\nrozzvučí síň úděsnými tóny waltzu,\ntanga a quickstepu.",
    "Tất cả mọi người sinh ra đều\nđược tự do và bình đẳng về\nnhân phẩm và quyền lợi.",
    "Kæmi ný öxi hér ykist þjófum\nnú bæði víl og ádrepa.",
    "דג סקרן שט בים מאוכזב ולפתע מצא חברה",
]

def update(img, help=False, a=0, ind=0, m=False, il=0):
    i:pyi.image = pyi.new_img(background=pyi.COL.black)
    i.text(strs[ind%len(strs)], [i/2 for i in pyi.RES.resolution], fontSize=40, thickness=2, anchor="mm", angle=a)
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
        if wk == ord("r"): a += 10
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