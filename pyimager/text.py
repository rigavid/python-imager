try: from pyimager.text_conv import *
except: from text_conv import *
try: from pyimager.chars import *
except: from chars import *
import unicodedata

class Text:
    class Chain:
        class Char: ## TODO Prevent overlapping accents
            X, Y = 5, 7
            TypeText, TypeControl, TypeFormat, TypeDiacritic, TypeUnknown = "T", "C", "F", "D", "U"
            TypeSymbol, TypeLetter, TypeEmoji = "S", "L", "E"
            def __init__(self, chr, style="", monospace=False):
                self.monospace = monospace
                if len(chr)>3 and chr.count(":") == 1: chr, self.args = chr.split(":")
                if chr in CONV: self.char = CONV[chr]
                else:
                    try: self.char = CONV[f"{ord(chr):0>4x}"] ## Hex value of ord(i)
                    except: self.char = chr if chr in CHARS else f"<{chr}>"
                self.diacr = False ## It is changed after it's definition by Chain.__init__()
                self.style = style
            def __str__(self):
                try: return f"{self.char}{self.style}:{self.args}"
                except: return f"{self.char}{self.style}"
            def split(self, *args, **kwargs):
                return self.__str__().split(*args, **kwargs)
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
                upper = not (self.__specific_type__()==self.TypeLetter and self.char[0] == "B")
                if len(self.char)==3 and self.char[0] == "A" and int(self.char[1::]) > 97: upper = False
                return upper
            def draw(self, img, pts, help=False, *args, **kwargs):
                if self.__type__() in [self.TypeText, self.TypeUnknown, self.TypeDiacritic] or self in ["00", "06"]:
                    draw_char(img, self, pts=pts, help=help, *args, **kwargs)
                elif self.__type__() == self.TypeControl and help:
                    img.polygon([*pts[:2:], *pts[:1:-1]], COL.yellow, 2, 2)
                    img.line(pts[0], pts[3], COL.yellow, 1, 2)
                    img.line(pts[1], pts[2], COL.yellow, 1, 2)
                    d = 3
                    img.circle(pts[0], d*2, COL.compl(COL.help), 0)
                    for p in pts[:-1:]: img.circle(p, d, COL.help, 0)
                    img.text(str(self), pts[0], COL.help, fontSize=3, thickness=2, centered=False)
            def __eq__(self, other):
                if type(other) == type(self): return self.char == other.char
                else: return self.char == str(other)
            def get_width_height(self): ## TODO Set chars' width
                XD, YD =  self.X, self.Y
                if self.monospace: return XD, YD
                match self.__type__():
                    case self.TypeControl:
                        match str(self.char):
                            case "00"|"06": XD *= 0.5
                            case "01": XD *= 0.6
                            case _: return XD, YD
                    case self.TypeFormat: return 0, YD
                    case self.TypeDiacritic: return self.width, YD
                    case self.TypeText:
                        match self.__specific_type__():
                            case self.TypeLetter:
                                l, n, u = self.char[0], int(self.char[1::]), self.__is_upper__()
                                if n < 30: ## LATIN ##
                                    if n in (26, 27): XD *= 1.1 if u else 0.75 ## Æ|Œ
                                    else: XD *= 0.9 if u else 0.6
                                elif n < 70: ## CYRILLIC ##
                                    XD *= 0.9 if u else 0.6
                                elif n < 100: ## GREEK ##
                                    XD *= 0.9 if u else 0.6
                            case self.TypeSymbol:
                                ...
                                # c, l, n = self.char, self.char[0], self.char[1]
                                # if (l=="B" and not n in "4579")or(l=="C"and n in "02"): XD *= 0.1
                                # if (l=="C" and n=="1")or(l=="D"and not n in "6789")or(l=="G"and n in "012"): XD *= 0.3
                return XD, YD
        def __init__(self, string="", monospace=False):
            string = string.replace("\r", "^05^").replace("\v", "^04^").replace("\n", "^05^^04^") \
                .replace("\b", "^07^").replace("\t", "^08^").replace("\f", "^09^").replace(" ", "^01^")
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
            chaine = []
            format = False
            bg = fg = ls = ul = tl = ol = it = bd = ci = tn = vm = hm = False
            for c in chars: ## Set styles ##
                char = self.Char(c, monospace=monospace)
                if char.__type__() == char.TypeFormat:
                    r = True
                    match char.char:
                        case "20":
                            bg = fg = ls = ul = tl = ol = it = bd = ci = tn = vm = hm = False if format else True
                            r = not format
                        case "21": ul = not ul
                        case "22": tl = not tl
                        case "23": ol = not ol
                        case "24": it = not it
                        case "25": bd = not bd
                        case "26": ci = not ci
                        case "27": tn = not tn
                        case "28": vm = not vm
                        case "29": hm = not hm
                        case "30":
                            try: bg, bg_c = not bg, char.args
                            except: bg = False
                        case "31":
                            try: fg, fg_c = not fg, char.args
                            except: bg = False
                        case "32":
                            try: ls, ls_c = not ls, char.args
                            except: bg = False
                    format = r
                else:
                    styles = []
                    if format and char.__type__() == char.TypeText:
                        styles = [
                            "UL" if ul else "",
                            "TL" if tl else "",
                            "OL" if ol else "",
                            "IT" if it else "",
                            "CI" if ci else "",
                            "BD" if bd else "",
                            "TN" if tn else "",
                            "VM" if vm else "",
                            "HM" if hm else "",
                            f"BG({bg_c})" if bg else "",
                            f"FG({fg_c})" if fg else "",
                            f"LS({ls_c})" if ls else ""
                        ]
                        char.style = ":"+":".join(i for i in styles if not i == "")
                    elif format and char.__type__() == char.TypeDiacritic:
                        styles = [
                            "IT" if it else "",
                            "CI" if ci else "",
                            "BD" if bd else "",
                            "TN" if tn else "",
                            "VM" if vm else "",
                            "HM" if hm else "",
                            f"FG({fg_c})" if fg else "",
                        ]
                        char.style = ":"+":".join(i for i in styles if not i == "")
                    chaine.append(char)
            self.string, self.chain = strg, chaine
            for char in self:
                ind = self.index
                try:
                    if char.__type__() == self.Char.TypeDiacritic:
                        nxt = next(self)
                        while nxt.__type__() == self.Char.TypeDiacritic:
                            nxt = next(self)
                        char.upper = nxt.__is_upper__()
                        char.width = nxt.get_width_height()[0]
                        nxt.diacr = True
                    else: char.upper = char.__is_upper__()
                except StopIteration: char.upper = char.__is_upper__()
                self.index = ind
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
    def __init__(self, text, monospace=False):
        self.text = self.Chain(str(text), monospace)
    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else: return self.text.string == str(other)
    def __str__(self):
        return str(self.text)
    def __type__str__(self):
        return self.text.__type__str__()
    def new_pt(self, pt, char, linept, orgpt, pos, fontSize, angle=0, interligne=0):
        XD, YD = char.get_width_height()
        XD *= fontSize; YD *= fontSize; YD += interligne
        if char.__type__() in (char.TypeDiacritic, char.TypeFormat): pass
        elif char.__type__ () == char.TypeControl:
            if   char == "02": pt = coosCircle(pt, XD, angle+180); pos[0] -= 1
            elif char == "03": pt = linept = coosCircle(pt, YD, angle+270); pos[1] -= 1
            elif char == "04": pt = linept = coosCircle(pt, YD, angle+ 90); pos[1] += 1
            elif char == "05": pt, pos[0] = linept, 0
            elif char == "07": pt, pos[1], linept = orgpt, 0, coosCircle(linept, YD*pos[1], angle+270)
            elif char == "08": n = 4-(pos[0]%4); pt = coosCircle(pt, XD*n, angle); pos[0] += n
            elif char == "09": n = 4-(pos[0]%4); pt = coosCircle(pt, XD*n, 180+angle); pos[0] -= n
            else: pt = coosCircle(pt, XD, angle); pos[0] += 1
        else: pt = coosCircle(pt, XD, angle); pos[0] += 1
        return pt, linept, orgpt, pos
    def get_cases(self, pt, fontSize, angle, interligne):
        pts, pos = [], [0, 0]
        linept = orgpt = pt
        for char in self.text:
            if char.__type__() == char.TypeControl:
                if not char.char in ("00", "01", "06"):
                    pts.append([pt, pt, pt, pt])
                    pt, linept, orgpt, pos = self.new_pt(pt, char, linept, orgpt, pos, fontSize, angle, interligne)
                    continue
            x, y = char.get_width_height()
            pts.append(
                [pt, coosCircle(pt, x*fontSize, angle), coosCircle(pt, y*fontSize, angle+90),
                coosCircle(pt, square_root(x*x+y*y)*fontSize, angle+angleInterPoints([0,0],[x,y]))])
            pt, linept, orgpt, pos = self.new_pt(pt, char, linept, orgpt, pos, fontSize, angle, interligne)
        return pts
    def get_size(self, fontSize=1, interligne=0):
        poses = self.get_cases((0, 0), fontSize, 0, interligne)
        axes = [[], []]
        for p in poses:
            axes[0] += [p[0][0], p[-1][0]]
            axes[1] += [p[0][1], p[-1][1]]
        x = diff(min(axes[0]), max(axes[0]))
        y = diff(min(axes[1]), max(axes[1]))
        return x, y
    def get_center(self, pt, fontSize=1, angle=0, interligne=0):
        x, y = self.get_size(fontSize, interligne)
        PT = pt[0]-x/2, pt[1]-y/2
        return coosCircle(pt, dist(pt, PT), angle+angleInterPoints(pt, PT))
    def draw(self, img, pt, colour, thickness=1, fontSize=1, interligne=0, lineType=0, angle=0, centered=True, help=False):
        interligne *= self.Chain.Char.Y*fontSize
        origin = self.get_center(pt, fontSize, angle, interligne) if centered else pt
        cases = self.get_cases(origin, fontSize, angle, interligne)
        for chr, pts in zip(self.text, cases):
            chr.draw(img, pts=pts, colour=colour, thickness=thickness, fontSize=fontSize, lineType=lineType, angle=angle, help=help)
            if help: img.polygon((pts[i] for i in (0, 1, 3, 2)), COL.orangeRed, 1)