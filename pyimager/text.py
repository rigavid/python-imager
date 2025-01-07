try: from pyimager.main import *
except: from main import *

## TODO ##
## Format char : LLXX (67600 charactères possibles) ##

CONV = {
    ## Re-checker le vieux carnet de prog et le prog cvt.py
    "AA00":" ", "AB00":"\t","AC00":"0", "AD00":"1", "AE00":"2", "AF00":"3", "AG00":"4", "AH00":"5", "AI00":"6", "AJ00":"7", "AK00":"8", "AL00":"9", "AM00":"+", "AN00":"-", "AO00":" ", "AP00":" ", "AQ00":" ",
    "AA01":"¿", "AB01":"?", "AC01":"A", "AD01":"B", "AE01":"C", "AF01":"D", "AG01":"E", "AH01":"F", "AI01":"G", "AJ01":"H", "AK01":"I", "AL01":"J", "AM01":"K", "AN01":"L", "AO01":"M", "AP01":"N", "AQ01":"O",
    "AA02":"¡", "AB02":"!", "AC02":"P", "AD02":"Q", "AE02":"R", "AF02":"S", "AG02":"T", "AH02":"U", "AI02":"V", "AJ02":"W", "AK02":"X", "AL02":"Y", "AM02":"Z", "AN02":"Æ", "AO02":" ", "AP02":"Ç", "AQ02":"Ñ",
    "AA03":" ", "AB03":" ", "AC03":"a", "AD03":"b", "AE03":"c", "AF03":"d", "AG03":"e", "AH03":"f", "AI03":"g", "AJ03":"h", "AK03":"x", "AL03":"j", "AM03":"k", "AN03":"l", "AO03":"m", "AP03":"n", "AQ03":"o",
    "AA04":"(", "AB04":")", "AC04":"p", "AD04":"q", "AE04":"r", "AF04":"s", "AG04":"t", "AH04":"u", "AI04":"v", "AJ04":"w", "AK04":"i", "AL04":"y", "AM04":"z", "AN04":"æ", "AO04":" ", "AP04":"ç", "AQ04":"ñ",
    "AA05":"[", "AB05":"]", "AC05":" ", "AD05":" ", "AE05":" ", "AF05":" ", "AG05":" ", "AH05":" ", "AI05":" ", "AJ05":" ", "AK05":" ", "AL05":" ", "AM05":" ", "AN05":" ", "AO05":" ", "AP05":" ", "AQ05":" ",
    "AA06":"{", "AB06":"}", "AC06":" ", "AD06":" ", "AE06":" ", "AF06":" ", "AG06":" ", "AH06":" ", "AI06":" ", "AJ06":" ", "AK06":" ", "AL06":" ", "AM06":" ", "AN06":" ", "AO06":" ", "AP06":" ", "AQ06":" ",
    "AA07":"<", "AB07":">", "AC07":" ", "AD07":" ", "AE07":" ", "AF07":" ", "AG07":" ", "AH07":" ", "AI07":" ", "AJ07":" ", "AK07":" ", "AL07":" ", "AM07":" ", "AN07":" ", "AO07":" ", "AP07":" ", "AQ07":" ",
    "AA08":"`", "AB08":"´", "AC08":" ", "AD08":" ", "AE08":" ", "AF08":" ", "AG08":" ", "AH08":" ", "AI08":" ", "AJ08":" ", "AK08":" ", "AL08":" ", "AM08":" ", "AN08":" ", "AO08":" ", "AP08":" ", "AQ08":" ",
    "AA09":"^", "AB09":"ˇ", "AC09":" ", "AD09":" ", "AE09":" ", "AF09":" ", "AG09":" ", "AH09":" ", "AI09":" ", "AJ09":" ", "AK09":" ", "AL09":" ", "AM09":" ", "AN09":" ", "AO09":" ", "AP09":" ", "AQ09":" ",
    "AA10":" ", "AB10":" ", "AC10":" ", "AD10":" ", "AE10":" ", "AF10":" ", "AG10":" ", "AH10":" ", "AI10":" ", "AJ10":" ", "AK10":" ", "AL10":" ", "AM10":" ", "AN10":" ", "AO10":" ", "AP10":" ", "AQ10":" ",
    "AA11":"¨", "AB11":" ", "AC11":" ", "AD11":" ", "AE11":" ", "AF11":" ", "AG11":" ", "AH11":" ", "AI11":" ", "AJ11":" ", "AK11":" ", "AL11":" ", "AM11":" ", "AN11":" ", "AO11":" ", "AP11":" ", "AQ11":" ",
    "AA12":" ", "AB12":" ", "AC12":" ", "AD12":" ", "AE12":" ", "AF12":" ", "AG12":" ", "AH12":" ", "AI12":" ", "AJ12":" ", "AK12":" ", "AL12":" ", "AM12":" ", "AN12":" ", "AO12":" ", "AP12":" ", "AQ12":" ",
    "AA13":" ", "AB13":" ", "AC13":" ", "AD13":" ", "AE13":" ", "AF13":" ", "AG13":" ", "AH13":" ", "AI13":" ", "AJ13":" ", "AK13":" ", "AL13":" ", "AM13":" ", "AN13":" ", "AO13":" ", "AP13":" ", "AQ13":" ",
    "AA14":" ", "AB14":" ", "AC14":" ", "AD14":" ", "AE14":" ", "AF14":" ", "AG14":" ", "AH14":" ", "AI14":" ", "AJ14":" ", "AK14":" ", "AL14":" ", "AM14":" ", "AN14":" ", "AO14":" ", "AP14":" ", "AQ14":" ",
}
CONV2 = {CONV[key]:key for key in CONV}

# print(f"{",\n\t".join(", ".join(f"\"A{l}{n:0>2}\":\" \"" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ") for n in range(11, 15))}")
a, b = 26*26*10*10, len(CONV)
print(f"{a}, {b} => {b/a:.2%} used")

def is_comp(chr): ## TODO @
    return False
def discomp(chr): ## TODO @
    return chr

class Text:
    class chain:
        def __init__(self, string=""):
            self.string = str(string)
            self.chain = self.enchain()
        def enchain(self):
            return ";".join(CONV2[char] if not is_comp(char) else ":".join(CONV2[comp] for comp in discomp(char)) for char in self.string)
        def unchain(self):
            return "".join(CONV[char] if not ":" in char else "".join(CONV[comp] for comp in char) for char in self.chain.split(";"))
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

a = Text("12")
print(a.text.chain, a.text.unchain())