try: from pyimager.chars import *
except: from chars import *
try: from pyimager._vars_.text_conv import CONV, CHARS
except:
    try: from _vars_.text_conv import CONV, CHARS
    except: from text_conv import CONV, CHARS
import unicodedata

class Text:
    class Chain:
        class Char:
            TypeText = "T"
            TypeControl = "C"
            TypeFormat = "F"
            TypeDiacritic = "D"
            TypeSymbol = "S"
            def __init__(self, chr):
                if chr.count(":") == 1: chr, self.args = chr.split(":")
                if chr in CONV: self.char = CONV[chr]
                else:
                    try: self.char = CONV[f"{ord(chr):0>4x}"] ## Hex value of ord(i)
                    except: self.char = chr if chr in CHARS else f"<{chr}>"
            def __str__(self):
                try: return f"{self.char}:{self.args}"
                except: return str(self.char)
            def __type__(self):
                if str(self.char).isnumeric():
                    if int(self.char) >= 0 and int(self.char) <  20: return self.TypeControl
                    elif int(self.char) <  40: return self.TypeFormat
                    elif int(self.char) < 100: return self.TypeDiacritic
                elif str(self.char).isalnum(): return self.TypeText
                else: return "U" # UNMAPPED
            def __specific_type(self):
                if t:=self.__type__() != self.TypeText: return t
                elif len(self) == 2: return self.TypeSymbol
            def draw(self, img, pts, *args, **kwargs):
                if self.__type__() == self.TypeText or self == "00":
                    draw_char(img, self.char, pts=pts, *args, **kwargs)
                elif self.__type__() == self.TypeDiacritic:
                    draw_diacr(img, self.char, pts=pts, *args, **kwargs)
            def __eq__(self, other):
                if type(other) == type(self): return self.char == other.char
                else: return self.char == str(other)
        def __init__(self, string=""):
            s, o, d = f"^{CONV["SPC"]}^", f"^{CONV["ORG"]}^", f"^{CONV["DWN"]}^"
            string = string.replace( " ", s).replace("\r", o).replace("\v", d).replace("\n", o+d)
            chr, chars, strg, char_ = False, [], "", ""
            for c in string:
                if chr:
                    if c == "^":
                        if char_ == "":
                            chars.append("^")
                        else:
                            chars.append(char_)
                            char_ = ""
                        chr = False
                    else:
                        char_ += c
                else:
                    if c=="^":
                        chr = True
                    else:
                        chars.extend(unicodedata.normalize("NFD", c))
                strg += c
            self.string, self.chain = strg, [self.Char(c) for c in chars]
        def __str__(self):
            return self.string
        def __type__str__(self):
            return ";".join(i.__type__() for i in self.chain)
        def __iter__(self):
            self.index = -1
            return self
        def __next__(self):
            self.index += 1
            if self.index == len(self.chain): raise StopIteration
            return self.chain[self.index]
    def __init__(self, text):
        if type(text) == type(self): text = str(text)
        self.text = self.Chain(text)
    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else: return self.text.string == str(other)
    def __str__(self):
        return str(self.text)
    def __type__str__(self):
        return self.text.__type__str__()
    def get_cases(self, pt, fontSize=1, angle=0):
        pts, maxs, s = [], [*pt, *pt], self.text
        d = square_root(7**2+5**2)*fontSize
        an = angleInterPoints([0,0],[5,7])
        X, Y = 5*fontSize, 7*fontSize
        linept = copy.deepcopy(pt)
        for char in self.text:
            move = True
            c = [pt, coosCircle(pt, X, angle), coosCircle(pt, Y, angle+90), coosCircle(pt, d, angle+an)]
            for x, y in c:
                if x>maxs[0]: maxs[0]=x
                if y>maxs[1]: maxs[1]=y
                if x<maxs[2]: maxs[2]=x
                if y<maxs[3]: maxs[3]=y
            pts.append(c)
            try:
                nxt = next(self.text)
                if nxt.__type__() != "T":
                    if not nxt in ["00", "01"]:
                        move = False
                        if nxt.__type__() == "C":
                            if nxt == "02": pt = coosCircle(pt, 5*fontSize, angle+180)
                            if nxt == "03":
                                pt = coosCircle(pt, 7*fontSize, angle-90)
                                linept = copy.deepcopy(pt)
                            if nxt == "04":
                                pt = coosCircle(pt, 7*fontSize, angle+90)
                                linept = copy.deepcopy(pt)
                            if nxt == "05": pt = linept
                if char.__type__() == "C" and not char in ["00", "01"]:
                    move = False
                self.text.index -= 1
            except StopIteration: self.text.index -= 1
            if move: pt = coosCircle(pt, 5*fontSize, angle)
        center = [moyenne(maxs[0], maxs[2]), moyenne(maxs[1], maxs[3])]
        return pts, center
    def draw(self, img, pt, colour, thickness=1, fontSize=1, lineType=0, angle=0, centered=True, help=False):
        cases, center = self.get_cases(pt, fontSize, angle)
        if centered: cases, _ = self.get_cases([pt[0]-(center[0]-pt[0]), pt[1]-(center[1]-pt[1])], fontSize, angle)
        for chr, pts in zip(self.text, cases):
            chr.draw(img, pts=pts, colour=colour, thickness=thickness, fontSize=fontSize, lineType=lineType, angle=angle, help=help)
if __name__ == "__main__":
    import os; os.system("clear")
    a = 100 + 26*10 + 26*100 # (0-99)+(A0-A9)+(A00-Z99)
    b = len(CONV);print(f"{a}, {b} => {b/a:.2%} used")

    a = Text("Ça ñon Æ^A27^")
    print(";".join(str(i) for i in a.text.chain), a.text.chain.__sizeof__(), len(a.text.chain))
    print(a.text.string, a.text.string.__sizeof__(), len(a.text.string))
    print(a.__type__str__())