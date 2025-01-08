try: from pyimager.main import *
except: from main import *

## TODO ##
## Format chaine C;C;C ##
## Format char : LLXX(:LX) (67600 charactères possibles) ##

CONV = {
    ## Re-checker le vieux carnet de prog et le prog cvt.py
    " ":"AA00","\t":"AB00", "0":"AC00", "1":"AD00", "2":"AE00", "3":"AF00", "4":"AG00", "5":"AH00", "6":"AI00", "7":"AJ00", "8":"AK00", "9":"AL00", "+":"AM00", "-":"AN00", " ":"AO00", " ":"AP00", " ":"AQ00",
    "¿":"AA01", "?":"AB01", "A":"AC01", "B":"AD01", "C":"AE01", "D":"AF01", "E":"AG01", "F":"AH01", "G":"AI01", "H":"AJ01", "I":"AK01", "J":"AL01", "K":"AM01", "L":"AN01", "M":"AO01", "N":"AP01", "O":"AQ01",
    "¡":"AA02", "!":"AB02", "P":"AC02", "Q":"AD02", "R":"AE02", "S":"AF02", "T":"AG02", "U":"AH02", "V":"AI02", "W":"AJ02", "X":"AK02", "Y":"AL02", "Z":"AM02", "Æ":"AN02", " ":"AO02", "Ç":"AP02", "Ñ":"AQ02",
    " ":"AA03", " ":"AB03", "a":"AC03", "b":"AD03", "c":"AE03", "d":"AF03", "e":"AG03", "f":"AH03", "g":"AI03", "h":"AJ03", "x":"AK03", "j":"AL03", "k":"AM03", "l":"AN03", "m":"AO03", "n":"AP03", "o":"AQ03",
    "(":"AA04", ")":"AB04", "p":"AC04", "q":"AD04", "r":"AE04", "s":"AF04", "t":"AG04", "u":"AH04", "v":"AI04", "w":"AJ04", "i":"AK04", "y":"AL04", "z":"AM04", "æ":"AN04", " ":"AO04", "ç":"AP04", "ñ":"AQ04",
    "[":"AA05", "]":"AB05", "Α":"AC05", "Β":"AD05", "Γ":"AE05", "Δ":"AF05", "Ε":"AG05", "Ζ":"AH05", "Η":"AI05", "Θ":"AJ05", "Ι":"AK05", "Κ":"AL05", "Λ":"AM05", "Μ":"AN05", "Ν":"AO05", "Ξ":"AP05", "Ο":"AQ05",
    "{":"AA06", "}":"AB06", "Π":"AC06", "Ρ":"AD06", "Σ":"AE06", " ":"AF06", "Τ":"AG06", "Υ":"AH06", "Φ":"AI06", "Χ":"AJ06", "Ψ":"AK06", "Ω":"AL06", " ":"AM06", " ":"AN06", " ":"AO06", " ":"AP06", " ":"AQ06",
    "<":"AA07", ">":"AB07", "α":"AC07", "β":"AD07", "γ":"AE07", "δ":"AF07", "ε":"AG07", "ζ":"AH07", "η":"AI07", "θ":"AJ07", "ι":"AK07", "κ":"AL07", "λ":"AM07", "μ":"AN07", "ν":"AO07", "ξ":"AP07", "ο":"AQ07",
    "`":"AA08", "´":"AB08", "π":"AC08", "ρ":"AD08", "σ":"AE08", "ς":"AF08", "τ":"AG08", "υ":"AH08", "φ":"AI08", "χ":"AJ08", "ψ":"AK08", "ω":"AL08", " ":"AM08", " ":"AN08", " ":"AO08", " ":"AP08", " ":"AQ08",
    "^":"AA09", "ˇ":"AB09", " ":"AC09", " ":"AD09", " ":"AE09", " ":"AF09", " ":"AG09", " ":"AH09", " ":"AI09", " ":"AJ09", " ":"AK09", " ":"AL09", " ":"AM09", " ":"AN09", " ":"AO09", " ":"AP09", " ":"AQ09",
    " ":"AA10", " ":"AB10", " ":"AC10", " ":"AD10", " ":"AE10", " ":"AF10", " ":"AG10", " ":"AH10", " ":"AI10", " ":"AJ10", " ":"AK10", " ":"AL10", " ":"AM10", " ":"AN10", " ":"AO10", " ":"AP10", " ":"AQ10",
    "¨":"AA11", " ":"AB11", " ":"AC11", " ":"AD11", " ":"AE11", " ":"AF11", " ":"AG11", " ":"AH11", " ":"AI11", " ":"AJ11", " ":"AK11", " ":"AL11", " ":"AM11", " ":"AN11", " ":"AO11", " ":"AP11", " ":"AQ11",
    " ":"AA12", " ":"AB12", " ":"AC12", " ":"AD12", " ":"AE12", " ":"AF12", " ":"AG12", " ":"AH12", " ":"AI12", " ":"AJ12", " ":"AK12", " ":"AL12", " ":"AM12", " ":"AN12", " ":"AO12", " ":"AP12", " ":"AQ12",
    " ":"AA13", " ":"AB13", " ":"AC13", " ":"AD13", " ":"AE13", " ":"AF13", " ":"AG13", " ":"AH13", " ":"AI13", " ":"AJ13", " ":"AK13", " ":"AL13", " ":"AM13", " ":"AN13", " ":"AO13", " ":"AP13", " ":"AQ13",
    " ":"AA14", " ":"AB14", " ":"AC14", " ":"AD14", " ":"AE14", " ":"AF14", " ":"AG14", " ":"AH14", " ":"AI14", " ":"AJ14", " ":"AK14", " ":"AL14", " ":"AM14", " ":"AN14", " ":"AO14", " ":"AP14", " ":"AQ14",
    ## Diacritiques (Format LX) ##
    "`":"A0", "´":"A1", " ":"A2", " ":"A3", " ":"A4", " ":"A5",
    "^":"B0", "ˇ":"B1", " ":"B2", " ":"B3", " ":"B4", " ":"B5",
    " ":"C0", " ":"C1", " ":"C2", " ":"C3", " ":"C4", " ":"C5",
    " ":"D0", " ":"D1", " ":"D2", " ":"D3", " ":"D4", " ":"D5",
}; CONV[" "]="AA00"#Over-write any space left by error

# print(f"{",\n\t".join(", ".join(f"\"A{l}{n:0>2}\":\" \"" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ") for n in range(11, 15))}")
a, b = 26*26*10*10, len(CONV)
print(f"{a}, {b} => {b/a:.2%} used")

def is_comp(chr): ## TODO @
    return not chr in CONV
def discomp(chr): ## TODO @
    return " "

class Text:
    class chain:
        def __init__(self, string=""):
            self.string = str(string)
            self.chain = self.enchain()
        def enchain(self):
            o = ""
            for char in self.string:
                if not is_comp(char): o+=CONV[char]
                else:
                    o+=":".join(CONV[comp] for comp in discomp(char))
                o+=";"
            return o[:-1:]
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

a = Text("à")
print(a.text.chain, a.text.string)