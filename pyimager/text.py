from pyimager.main import *

## TODO

class Text:
    def encode(self, t): return t
    def decode(self, t): return t
    def __init__(self, text):
        self.text = self.encode(text)
    def __eq__(self, other):
        if type(self) == type(other):
            return self.text == other.text
        else:
            return self.decode(self.text) == str(other)
    def __str__(self): return self.decode(self.text)