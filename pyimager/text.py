import unicodedata

CONV = {# Characters (Format LLXX) (67600 charactères possibles) #
    ## Control characters ## INDex, RiGhT, LeFT, UP, DoWN, ORiGin, END, TOP, BoTtoM, BacKSpace, DELete, TABulation, SPaCe
    "IND":"00", "RGT":"01", "LFT":"02", "UPP":"03", "DWN":"04", "ORG":"05", "END":"06", "TOP":"07", "BTM":"08", "BKS":"09",
    "DEL":"10", "TAB":"11", "SPC":"12", "   ":"13", "   ":"14", "   ":"15", "   ":"16", "   ":"17", "   ":"18", "   ":"19",
    ## Format  characters ## UNformat, UnderLine, TopLine, OverLine, ITalic, BolD, Counter-Italic, ThiN, Vertical Mirror, Horizontal Mirror, BackGround, ForeGround, LineS
    "UN":"20", "UL":"21", "TL":"22", "OL":"23", "IT":"24", "BD":"25", "CI":"26", "TN":"27", "VM":"28", "HM":"29",
    "BG":"30", "FG":"31", "LS":"32", "  ":"33", "  ":"34", "  ":"35", "  ":"36", "  ":"37", "  ":"38", "  ":"39",
    ## Text characters
    ### Diacritics chars
    #### Suscrit ## Le double grave ne se voit pas bien, mais il est bien la ! ##
    "0300":"40", "´":"41", "^":"42", "ˇ":"43", "˝":"44", " ̏":"45", "¨":"46", "˙":"47", "˘":"48", "¯":"49",
    "˜":"50", "ˈ":"51", " ":"52", " ":"53", " ":"54", " ":"55", " ":"56", " ":"57", " ":"58", " ":"59",
    #### Souscrit ##
    "¸":"60", "˛":"61", "ˌ":"62", "◌̣":"63", " ":"64", " ":"65", " ":"66", " ":"67", " ":"68", " ":"69",
    " ":"70", " ":"71", " ":"72", " ":"73", " ":"74", " ":"75", " ":"76", " ":"77", " ":"78", " ":"79",
    #### Inscrit ##
    " ":"80", " ":"81", "ˌ":"82", "◌̣":"83", " ":"84", " ":"85", " ":"86", " ":"87", " ":"88", " ":"89",
    " ":"90", " ":"91", " ":"92", " ":"93", " ":"94", " ":"95", " ":"96", " ":"97", " ":"98", " ":"99",
    ### Base chars ##
    "0041":"A0", "":"A1", "":"A2", "":"A3", "":"A4", "":"A5", "":"A6", "":"A7", "":"A8", "":"A9", "":"A10",
}; CONV["\n"] = f"{CONV["ORG"]};{CONV["DWN"]}"

# print(f"{",\n\t".join(", ".join(f"\"A{l}{n:0>2}\":\" \"" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ") for n in range(11, 15))}")
a, b = 100+26*10, len(CONV)
print(f"{a}, {b} => {b/a:.2%} used")

class Text:
    class chain:
        class char:
            def __init__(self, chr):
                try: self.char = CONV[chr]
                except: self.char = f".{chr}" # self.char = UNMAPPED CHARACTER!
            def __str__(self):
                return str(self.char)
            def __type__(self):
                print(self.char, str(self.char).isalpha(), str(self.char).isnumeric(), str(self.char).isalnum())
                if str(self.char).isnumeric():
                    if int(self.char) >= 0 and int(self.char) <  20: return "CONTROL"
                    elif int(self.char) <  40: return "FORMAT"
                    elif int(self.char) < 100: return "DIACRITIC"
                elif str(self.char).isalnum(): return "TEXT"
                else: return "UNMAPPED"
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
                    for i in unicodedata.normalize("NFD", c):
                        x = f"{ord(i):0>4x}"
                        print(x)
                        chars.append(x)
                    strg += c
            print(string, chars)
            self.string = strg
            self.chain = [(self.char(c)) for c in chars]
        def __str__(self):
            return self.string
        def __type__str__(self):
            return ";".join(i.__type__() for i in self.chain)
    def __init__(self, text):
        self.text = self.chain(text)
    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else: return self.text.string == str(other)
    def __str__(self):
        return str(self.text)
    def __type__str__(self):
        return self.text.__type__str__()

a = Text("À^SPC^Q!\"^BG^")
print(a.text.chain, a.text.chain.__sizeof__(), len(a.text.chain))
print(a.text.string, a.text.string.__sizeof__(), len(a.text.string))
print(a.__type__str__())