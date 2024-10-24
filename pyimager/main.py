import os, cv2, copy, numpy as np, random as rd

try: from pyimager.resolution import resolution as RES
except: from resolution import resolution as RES
try: from pyimager.colors import colour as COL
except: from colors import colour as COL

def debug_decorator(funct):
    def inner(*args, **kwargs):
        try: return funct(*args, **kwargs)
        except Exception as e:
            print(args, kwargs)
            raise e
    return inner

class image:
    class button: ## TODO ##
        def __init__(self, name="", coos=[[0,0], RES.resolution]) -> None: ...
        def on_click(self) -> None: ...
    def new_image(self=None, dimensions=RES.resolution, fond=COL.white) -> np.array:
        '''New image'''
        return np.full([round(v) for v in dimensions[::-1]]+[3], fond[::-1], np.uint8)
    def __init__(self, name="python-image", img=None) -> None:
        self.name, self.img = name, np.array(self.new_img() if type(img) == type(None) else img.img if type(img) == image else img)
        self.callback, self.fullscreen = None, False