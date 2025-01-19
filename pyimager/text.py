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
            X, Y = 5, 7
            TypeText, TypeControl, TypeFormat, TypeDiacritic, TypeUnknown = "T", "C", "F", "D", "U"
            TypeSymbol, TypeLetter, TypeEmoji = "S", "L", "E"
            def __init__(self, chr):
                if len(chr)>3 and chr.count(":") == 1: chr, self.args = chr.split(":")
                if chr in CONV: self.char = CONV[chr]
                else:
                    try: self.char = CONV[f"{ord(chr):0>4x}"] ## Hex value of ord(i)
                    except: self.char = chr if chr in CHARS else f"<{chr}>"
                self.diacr = False ## It is changed after it's definition by Chain.__init__()
            def __str__(self):
                try: return f"{self.char}:{self.args}"
                except: return str(self.char)
            def __type__(self):
                if str(self.char).isnumeric():
                    if int(self.char) >= 0 and int(self.char) <  20: return self.TypeControl
                    elif int(self.char) <  40: return self.TypeFormat
                    elif int(self.char) < 100: return self.TypeDiacritic
                elif str(self.char).isalnum(): return self.TypeText
                else: return self.TypeUnknown
            def __len__(self):
                return len(self.char)
            def __specific_type__(self):
                if t:=self.__type__() != self.TypeText: return t
                elif len(self) == 2: return self.TypeSymbol
                elif len(self) == 3: return self.TypeLetter
                elif len(self) == 4: return self.TypeEmoji
                else: return self.TypeUnknown
            def __is_upper__(self):
                return not (self.__specific_type__()==self.TypeLetter and self.char[0] == "B")
            def draw(self, img, pts, *args, **kwargs):
                if self.__type__() in [self.TypeText, self.TypeUnknown, self.TypeDiacritic] or self in ["00", "06"]:
                    draw_char(img, self, pts=pts, format={}, *args, **kwargs)
                elif self.__type__() == self.TypeControl and False:
                    img.polygon([*pts[:2:], *pts[:1:-1]], COL.yellow, 3, 2)
                    img.line(pts[0], pts[3], COL.yellow, 3, 2)
                    img.line(pts[1], pts[2], COL.yellow, 3, 2)
            def __eq__(self, other):
                if type(other) == type(self): return self.char == other.char
                else: return self.char == str(other)
        def __init__(self, string=""):
            s, o, d, tp, tb, rtb = f"^{CONV["SPC"]}^", f"^{CONV["ORG"]}^", f"^{CONV["DWN"]}^", f"^{CONV["TOP"]}^", f"^{CONV["TAB"]}^", f"^{CONV["RTB"]}^"
            string = string.replace(" ", s).replace("\r", o).replace("\v", d).replace("\n", o+d).replace("\b", tp).replace("\t", tb).replace("\f", rtb)
            chr, chars, strg, char_ = False, [], "", ""
            for c in string:
                if chr:
                    if c == "^":
                        if char_ == "": chars.append("^")
                        else:
                            chars.append(char_)
                            char_ = ""
                        chr = False
                    else: char_ += c
                else:
                    if c=="^": chr = True
                    else: ## chars[::-1] car unicode donne le char, puis le diacr, tandis qu'on écrit premier le diacr, aussi, écrit-on le char.
                        if unicodedata.category(c) == "Mn": c = f"{chars.pop(-1)}{c}"
                        chars.extend(unicodedata.normalize("NFD", c)[::-1])
                strg += c
            self.string, self.chain = strg, [self.Char(c) for c in chars]
            for char in self:
                if char.__type__() == self.Char.TypeDiacritic:
                    try:
                        nxt = next(self)
                        char.upper = nxt.__is_upper__()
                        nxt.diacr = True
                    except StopIteration: char.upper = False
                    self.index -= 1
        def __len__(self):
            return len(self.chain)
        def __str__(self):
            return self.string
        def __type__str__(self):
            return ";".join(i.__type__() for i in self.chain)
        def __chain__str__(self):
            return ";".join(str(i) for i in self.chain)
        def __iter__(self):
            self.index = -1
            return self
        def __next__(self):
            self.index += 1
            if self.index == len(self): raise StopIteration
            return self.chain[self.index]
    def __init__(self, text):
        self.text = self.Chain(str(text))
    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else: return self.text.string == str(other)
    def __str__(self):
        return str(self.text)
    def __type__str__(self):
        return self.text.__type__str__()
    def new_pt(self, pt, char, linept, orgpt, pos, fontSize, angle=0):
        if char.__type__() in (char.TypeDiacritic, char.TypeFormat):
            pass
        elif char.__type__ () == char.TypeControl:
            if   char == "02":
                pos[0] -= 1
                pt = coosCircle(pt, self.Chain.Char.X*fontSize, angle+180)
            elif char == "03":
                pos[1] -= 1
                pt, linept = coosCircle(pt, self.Chain.Char.Y*fontSize, angle+270), coosCircle(linept, self.Chain.Char.Y*fontSize, angle+270)
            elif char == "04":
                pos[1] += 1
                pt, linept = coosCircle(pt, self.Chain.Char.Y*fontSize, angle+ 90), coosCircle(linept, self.Chain.Char.Y*fontSize, angle+ 90)
            elif char == "05": pt, pos[0], orgpt = linept, 0, coosCircle(orgpt, self.Chain.Char.X*fontSize*pos[0], angle+180)
            elif char == "07": pt, pos[1], linept = orgpt, 0, coosCircle(linept, self.Chain.Char.Y*fontSize*pos[1], angle+270)
            elif char == "08":
                n = 4-(pos[0]%4)
                pt, orgpt = coosCircle(pt, self.Chain.Char.X*fontSize*n, angle), coosCircle(orgpt, self.Chain.Char.X*fontSize*n, angle)
                pos[0] += n
            elif char == "09":
                n = 4-(pos[0]%4)
                pt, orgpt = coosCircle(pt, self.Chain.Char.X*fontSize*n, 180+angle), coosCircle(orgpt, self.Chain.Char.X*fontSize*n, 180+angle)
                pos[0] -= n
            else:
                pt, orgpt = coosCircle(pt, self.Chain.Char.X*fontSize, angle), coosCircle(orgpt, self.Chain.Char.X*fontSize, angle)
                pos[0] += 1
        else:
            pt, orgpt = coosCircle(pt, self.Chain.Char.X*fontSize, angle), coosCircle(orgpt, self.Chain.Char.X*fontSize, angle)
            pos[0] += 1
        return pt, linept, orgpt, pos
    def get_center(self, pt, fontSize=1, angle=0):
        x, y = self.Chain.Char.X, self.Chain.Char.Y
        maxs, pos = [0, 0, 0, 0], [0, 0]
        for char in self.text:
            match char.__type__():
                case char.TypeControl:
                    match str(char):
                        case a if a in ("00", "01", "06"): pos[0] += 1
                        case "02": pos[0] -= 1
                        case "03": pos[1] -= 1
                        case "04": pos[1] += 1
                        case "05": pos[0] = 0
                        case "07": pos[1] = 0
                        case "08": pos[0] += 4-(pos[0]%4)
                        case "09": pos[0] -= 4-(pos[0]%4)
                case char.TypeFormat: continue
                case char.TypeDiacritic: continue
                case char.TypeText: pos[0] += 1
            if pos[0]>maxs[0]: maxs[0]=pos[0]
            if pos[1]>maxs[1]: maxs[1]=pos[1]
            if pos[0]<maxs[2]: maxs[2]=pos[0]
            if pos[1]<maxs[3]: maxs[3]=pos[1]
        bords = [coosCircle(coosCircle(pt, x*maxs[2]*fontSize, 180+angle), y*maxs[3]*fontSize, 270+angle), coosCircle(coosCircle(pt, x*maxs[0]*fontSize, angle), y*maxs[1]*fontSize, 90+angle)]
        c = coosCircle(ct_sg(*bords), self.Chain.Char.Y*fontSize/2, angle+90)
        c2 = ((pt[0]-c[0]), (pt[1]-c[1]))
        return (pt[0]+c2[0], pt[1]+c2[1])
    def get_cases(self, pt, fontSize=1, angle=0):
        pts, s, x, y = [], self.text, self.Chain.Char.X, self.Chain.Char.Y
        pos = [0, 0]
        linept = orgpt = pt
        d, X, Y, an = square_root(x*x+y*y)*fontSize, x*fontSize, y*fontSize, angleInterPoints([0,0],[x,y])
        for char in self.text:
            pts.append([pt, coosCircle(pt, X, angle), coosCircle(pt, Y, angle+90), coosCircle(pt, d, angle+an)])
            pt, linept, orgpt, pos = self.new_pt(pt, char, linept, orgpt, pos, fontSize, angle)
        return pts
    def draw(self, img, pt, colour, thickness=1, fontSize=1, lineType=0, angle=0, centered=True, help=False):
        center = self.get_center(pt, fontSize, angle) if centered else pt
        cases = self.get_cases(center, fontSize, angle)
        for chr, pts in zip(self.text, cases):
            chr.draw(img, pts=pts, colour=colour, thickness=thickness, fontSize=fontSize, lineType=lineType, angle=angle, help=help)

if __name__ == "__main__":
    import os
    os.system("clear")
    used, total = len(CONV), 100 + 26*10 + 26*100 # (0-99)+(A0-A9)+(A00-Z99)
    print(f"{used:0>4}/{total} => {used/total:.2%} used")

    a = Text("Ça ñon Æ^A27^")
    print(";".join(str(i) for i in a.text.chain), a.text.chain.__sizeof__(), len(a.text.chain))
    print(a.text.string, a.text.string.__sizeof__(), len(a.text.string))
    print(a.__type__str__())