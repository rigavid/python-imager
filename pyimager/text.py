## TODO ##
## Format chaine C;C;C ##
## Format char : LLXX(:LX) (67600 charactères possibles) ##

CONV = { # Re-checker le vieux carnet de prog et le prog cvt.py
    # Characters (Format LLXX) (67600 charactères possibles) #
    ## Control characters
    "INDEX":"c0", "RIGHT":"c1", "LEFT":"c2", "UP":"c3", "DOWN":"c4", "ORIGIN":"c5", "END":"c6", "TOP":"c7", "BOTTOM":"c8", "BACKSPACE":"c9", "DELETE":"c10", "TAB":"c11",
    ## Format characters (Except color changers, because they have args)
    "UN":"f0", "UL":"f1", "TL":"f2", "OL":"f3", "IT":"f4", "BD":"f5", "CI":"f6", "TN":"f7", "MV":"f8", "MH":"f9",
    ## Text chars
    ### Base chars
    "":"A0", "":"A1", "":"A2", "":"A3", "":"A4", "":"A5", "":"A6", "":"A7", "":"A8", "":"A9", "":"A10",
    ### Diacritics chars (Format LX) (>260 diacritiques possibles) #
    "`":"d0", "´":"d1", "^":"d2", "¨":"d3", "°":"d4", "ˇ":"d5", "¯":"d6", "˛":"d7", "˘":"d8",
}; CONV[" "]="AA00"#Over-write any space left by error
CONV["\n"] = f"{CONV["ORIGIN"]};{CONV["DOWN"]}"

# print(f"{",\n\t".join(", ".join(f"\"A{l}{n:0>2}\":\" \"" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ") for n in range(11, 15))}")
a, b = 26*26*10*10, len(CONV)
print(f"{a}, {b} => {b/a:.2%} used")

class Text:
    class chain:
        class char:
            def __init__(self, chr):
                try: self.char = CONV[chr]
                except: self.char = chr # self.char = UNMAPPED CHARACTER!
            def __str__(self):
                return str(self.char)
        def __init__(self, string=""):
            chr = False
            chars, strg, char_ = [], "", ""
            for c in string:
                if c == "^" and chr:
                    if char_ != "": chars.append(char_)
                    else:
                        chars.append("^")
                        strg += "^"
                    chr, char_ = False, ""
                elif chr: char_ += c
                elif c=="^": chr = True
                else:
                    strg += c
                    chars.append(c)
            print(string, chars)
            self.string = strg
            self.chain = ";".join(str(self.char(c)) for c in chars)
        def __str__(self):
            return self.string
    def __init__(self, text):
        self.text = self.chain(text)
    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else:
            return self.text.string == str(other)
    def __str__(self):
        return self.text.__str__()

a = Text("HELLO WORLD ^INDEX^")
print(a.text.string, a.text.chain.__sizeof__(), a.text.chain)
print(a.text.chain, a.text.string.__sizeof__(), a.text.string)