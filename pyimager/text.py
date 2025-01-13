try: from pyimager.main import *
except: from main import *
try: from pyimager._vars_.text_conv import CONV, CHARS
except:
    try: from _vars_.text_conv import CONV, CHARS
    except: from text_conv import CONV, CHARS
import unicodedata

class Text:
    class chain:
        class char:
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
                    if int(self.char) >= 0 and int(self.char) <  20: return "C" # CONTROL
                    elif int(self.char) <  40: return "F" # FORMAT
                    elif int(self.char) < 100: return "D" # DIACRITIC
                elif str(self.char).isalnum(): return "T" # TEXT
                else: return "U" # UNMAPPED
            def draw(self, pts, colour, thickness=1, lineType=0): ...
        def __init__(self, string=""):
            string = string.replace( " ", "^SPC^").replace("\r", "^ORG^").replace("\v", "^DWN^").replace("\f", "^BTM^")
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
            self.string, self.chain = strg, [self.char(c) for c in chars]
        def __str__(self):
            return self.string
        def __type__str__(self):
            return ";".join(i.__type__() for i in self.chain)
    def __init__(self, text):
        if type(text) == type(self):
                text = str(text)
        self.text = self.chain(text)
    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else: return self.text.string == str(other)
    def __str__(self):
        return str(self.text)
    def __type__str__(self):
        return self.text.__type__str__()
    def get_cases(self, pt, fontSize=1):
        pts, s = [], self.chain
    def draw(self, img, pt, colour, thickness=1, fontSize=1, lineType=0):
        for chr, pts in zip(self.chain, self.get_cases(pt, fontSize)):
            chr.draw()

if __name__ == "__main__":
    import os; os.system("clear")
    a = 100 + 26*10 # (0-99)+(A0-A9)+(A00-Z99)
    b = len(CONV);print(f"{a}, {b} => {b/a:.2%} used")

    a = Text("Ça ñon Æ^A27^")
    print(";".join(str(i) for i in a.text.chain), a.text.chain.__sizeof__(), len(a.text.chain))
    print(a.text.string, a.text.string.__sizeof__(), len(a.text.string))
    print(a.__type__str__())