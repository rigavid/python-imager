try: from main import *
except: from pyimager.main import *

if __name__ == "__main__":
    img = image().build()
    img.show(0)