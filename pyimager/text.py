from pyimager.main import *

## TODO ##
## Format char : LLXX ##
CONV = {
    "AA00":"a", "AA01":"b" ## Re-checker le vieux carnet de prog et le prog cvt.py
}

class Text:
    class chain:
        def __init__(self, string=""):
            self.string = string
            self.chain = self.enchain()
        def enchain(self):
            for char in self.string:...

        def __str__(self):
            return self.string

    def __init__(self, text):
        self.text = self.chain(text)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else:
            return self.decode(self.text) == str(other)

    def __str__(self):
        return self.text.__str__()