import os, cv2, copy, numpy as np, random as rd
try: from pyimager.__vars__ import *
except: from __vars__ import *

# Mandatory for Fedora, works on Windows too # TODO see if it works on other distros
try: os.environ["XDG_SESSION_TYPE"] = "xcb"
except: ...

class unreachableImage(Exception):...
def debug_decorator(funct):
    def inner(*args, **kwargs):
        try: return funct(*args, **kwargs)
        except Exception as e:
            print(args, kwargs)
            raise e
    return inner
def fusionImages(img, base_img, pos=[0, 0]):
    '''Place an image over another'''
    pos = [round(v) for v in pos]
    x_offset, y_offset = pos
    try:
        base_img[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
        return base_img
    except (IndexError, ValueError):
        sz_x, sz_y = len(img[0]), len(img)
        for x_ in range(sz_x):
            x = pos[0]+x_
            if x<0 or x>=len(base_img[0]): continue
            for y_ in range(sz_y):
                y = pos[1]+y_
                if y<0 or y>=len(base_img): continue
                base_img[y,x] = img[y_,x_]
        return base_img
def new_img(dimensions=RES.resolution, background=COL.white, name="NewImg") -> np.array:
    return image(name, image.new_image(dimensions=dimensions, background=background))
class image:
    class button: ## TODO ##
        def __init__(self, name="", coos=[[0,0], RES.resolution]) -> None: ...
        def on_click(self) -> None: ...
    def new_image(self=None, dimensions=RES.resolution, background=COL.white) -> np.array:
        '''New image'''
        return np.full([round(v) for v in dimensions[::-1]]+[3], background[::-1], np.uint8)
    def __init__(self, name="python-image", img=None) -> None:
        self.img = np.array(self.new_image() if type(img) == type(None) else img.img if type(img) == image else img)
        self.name, self.fullscreen = name, False
        return
    def __str__(self) -> str: return self.name
    def show(self, wait=1, destroy=False, build_in_functs=True) -> int:
        '''Show image in a window'''
        if self.fullscreen:
            cv2.namedWindow(self.name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
        else:
            cv2.namedWindow(self.name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_KEEPRATIO)
        cv2.imshow(self.name, np.array(self.img, np.uint8))
        wk = cv2.waitKeyEx(wait)
        if destroy == True: cv2.destroyWindow(self.name)
        elif build_in_functs:
            match wk:
                case 65470: cv2.moveWindow(self.name, 0, 0) #f1
                case 65471: cv2.moveWindow(self.name, screen[0], 0) #f2
                case 32: self.fullscreen = not self.fullscreen #spacebar
                case 27: self.close()
                case _: return wk
            return -1
        return wk
    def build(self) -> None: return self.show(1, False, False)
    def is_closed(self) -> bool:
        '''Detect if the window is currently closed'''
        try: return cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1
        except: return True
    def is_opened(self) -> bool:
        '''Detect if the window is currently opened'''
        return not self.is_closed()
    def close(self) -> None:
        '''Closes window'''
        if not self.is_closed(): cv2.destroyWindow(self.name)
        return
    def setMouseCallback(self, funct, params=None) -> None:
        '''event, x, y, flags, params -> None'''
        if self.is_opened(): return cv2.setMouseCallback(self.name, funct, params)
        else: raise unreachableImage("Maybe you forgot to build the image?")
    def line(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a line on the image'''
        return cv2.line(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness), [cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA][lineType%3])
    def rectangle(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a rectangle on the image'''
        return cv2.rectangle(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness) if thickness != 0 else -1, [cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA][lineType%3])
    def polygon(self, pts=[ct_sg(p3, ct), ct_sg(p4, ct), ct_sg(ct, ch)], couleur=COL.black, thickness=1, lineType=0):
        '''Draws a polygon on the image'''
        pts = [[round(i) for i in pt] for pt in pts]
        lineType = [cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA][lineType%3]
        couleur = couleur[::-1]; thickness = int(thickness)
        if thickness > 0: cv2.polylines(self.img, [np.array(pts, dtype=np.int32)], True, couleur, thickness, lineType)
        else: cv2.fillPoly(self.img, [np.array(pts, np.int32)], couleur, lineType)
        return
    def circle(self, ct, rayon=10, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a circle on the image'''
        return cv2.circle(self.img, [round(p) for p in ct], round(rayon), colour[::-1], round(thickness) if thickness != 0 else -1, [cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA][lineType%3])
    def ellipse(self, ct, rayons=[10, 10], colour=COL.black, ep=1, lineType=0, anD=0, anF=360, ang=0) -> None:
        '''Draws an ellipse on the image'''
        return cv2.ellipse(self.img, [round(p) for p in ct], [round(i) for i in rayons], ang, anD, anF, colour[::-1], round(ep) if ep != 0 else -1, [cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA][lineType%3])
    def save_img(self, path='', fileName=None) -> None:
        '''Saves file'''
        if fileName == None: fileName = self.name
        if path != '': r = os.getcwd(); os.chdir(path)
        cv2.imwrite(fileName, self.img)
        if path != '': os.chdir(r)
        return
    def open_img(self, path) -> None:
        '''Opens local file as image'''
        self.img = cv2.imdecode(np.asarray(bytearray(open(f'{path}', "rb").read()), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        return
    def set_img(self, img) -> None:
        '''Sets the actual image to img'''
        self.img = np.array(img, np.uint8)
        return
    def write_centered(self, text, ct, colour=COL.red, thickness=1, fontSize=1, font=cv2.FONT_HERSHEY_SCRIPT_COMPLEX, lineType=0) -> None:
        '''Write over the image'''
        x1, y1 = ct; x2, y2 = ct; thickness = round(thickness)
        texts = list(enumerate(str(text).split('\n')))
        x, y = (x1+x2)/2, (y1+y2)/2 - round(cv2.getTextSize('Agd', font, fontSize, thickness)[0][1]*(len(texts)-1))
        for i, line in texts:
            tailles = cv2.getTextSize(line, font, fontSize, thickness)
            cv2.putText(self.img, line, (round(x-tailles[0][0]/2), round(y+tailles[1]/2) + i*tailles[0][1]*2), font, fontSize, colour[::-1], thickness, [cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA][lineType%3])
    def write(self, text, pt, colour=COL.red, thickness=1, fontSize=1, font=cv2.FONT_HERSHEY_SCRIPT_COMPLEX, lineType=0) -> None:
        cv2.putText(self.img, text, pt, font, fontSize, colour[::-1], thickness, [cv2.LINE_4, cv2.LINE_8, cv2.LINE_AA][lineType%3])
    def copy(self):
        '''Returns a copy of itself'''
        return image(self.nom, copy.deepcopy(self.img))
    def size(self, rev=False) -> [int, int]:
        '''Returns image's size (reverse True means [y,x] whereas False means [x,y])'''
        return [len(self.img[0]), len(self.img)][::-1 if rev else 1]
class layout:
    class Frame:
        def __init__(self, img=new_img(background=COL.white), pos=[0,0], name='frame0') -> None:
            self.name, self.img, self.pos = name, img.copy(), pos
            return
        def __str__(self) -> str:
            return self.name
    def __init__(self, img=new_img(), frames=[], name="Layout") -> None:
        self.name, self.img, self.frames = name, img.copy(), frames
        return
    def frame(self, img=new_img([100, 100], COL.white), pos=[0,0], name=None):
        if name == None: name = 'Unnamed_frame'
        frame_ = self.Frame(img=img, pos=pos, name=name)
        self.frames.append(frame_)
        return frame_
    def show(self, borders=False, frames=None, except_frames=[], fullscreen=True, build_in_functs=False):
        img = self.img.copy()
        if frames == None: frames = copy.deepcopy(self.frames)
        for frm in except_frames:
            ind = [i.name for i in frames].index(frm.name)
            if ind != -1: frames.pop(ind)
        for frame in frames:
            img.img = fusionImages(frame.img.img, img.img, frame.pos)
            if type(borders) in [int, float]:
                img.rectangle(frame.pos, [frame.pos[0]+len(frame.img.img[0]), frame.pos[1]+len(frame.img.img)], borders, 3, 2)
        return img.show(1, build_in_functs=build_in_functs)
    def is_closed(self) -> bool:
        '''Detect if the layout is currently closed'''
        return self.img.is_closed()
    def is_opened(self) -> bool:
        '''Detect if the layout is currently opened'''
        return self.img.is_opened()
    def size(self) -> [int, int]:
        return self.img.size()

def demo():
    img = new_img(background=COL.black, name="Demo")
    pt = pt_sg([0, 0], screen)
    img.ellipse(pt, [500, 100], COL.magenta, 10, 2)
    img.line([0, 0], screen, COL.white, 10, 2)
    img.circle([0, 0], 100, COL.red, 0, 2)
    img.circle(screen, 1000, COL.red, 0, 2)
    fs = True
    img.build()
    while img.is_opened(): img.show(1)
    return img

if __name__ == "__main__":
    demo()