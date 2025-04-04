import os, copy, numpy as np, random as rd
try: from pyimager.__vars__ import *
except: from __vars__ import *
try: from pyimager.text import Text
except: from text import Text

# Mandatory for Fedora, works on Windows too # TEST see if it works on other distros
try: os.environ["XDG_SESSION_TYPE"] = "xcb"
except: ...

class unreachableImage(Exception):...
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
def new_img(dimensions=None, background=COL.white, name="NewImg") -> np.array:
    return image(name, image.new_image(dimensions=dimensions if dimensions!=None else RES.resolution, background=background))
class image:
    class mouse:
        new = False
        event = x = y = flags = None
        def get(event, x, y, flags, _):
            image.mouse.new = True
            image.mouse.event = event
            image.mouse.x, image.mouse.y = x, y
            image.mouse.flags = flags
            return event, x, y, flags
    class button_:
        def __init__(self, name="", coos=[[100,100], [300, 200]]) -> None:
            self.name, self.coos = name, coos
            self.functs = []
        def defImg(self, img) -> None: self.img = img
        def draw(self, colour=COL.red, colour2=COL.darkRed, frameThickness=3, text="", **kwargs) -> None:
            self.img.rectangle(*self.coos, colour, 0, 2)
            self.img.rectangle(*self.coos, colour2, frameThickness, 2)
            if text != "": self.img.text(text, ct_sg(*self.coos), **kwargs)
        def on_click(self, funct, params=None) -> None:
            '''To add a function to execute when clicked'''
            self.functs.append([funct, params])
        def clicked(self, vars_get) -> None:
            '''Execute each function'''
            for f, p in self.functs: f(*vars_get, p)
        def is_clicked(self, coos) -> bool: return clicked_in(coos, self.coos)
    def button(self, name, coos=[[100,100], [300, 200]], *args, **kwargs) -> button_:
        bttn = self.button_(name, coos)
        bttn.defImg(self)
        bttn.draw(*args, **kwargs)
        self.buttons.append(bttn)
        return bttn
    def remove_button(self, bttn) -> button_ | int:
        try: return self.buttons.pop(self.buttons.index(bttn))
        except: return -1
    def setMouseCallback(self, funct, params=None) -> None:
        '''event, x, y, flags, params -> None'''
        self.callbacks.append([funct, params])
    def new_image(self=None, dimensions=RES.resolution, background=COL.white) -> np.array:
        '''New image'''
        return np.full([round(v) for v in dimensions[::-1]]+[3], background[::-1], np.uint8)
    def __init__(self, name="python-image", img=None, disable_callback=False) -> None:
        self.img = np.array(self.new_image() if type(img) == type(None) else img.img if type(img) == image else img)
        self.name, self.fullscreen = name, False
        self.buttons, self.callbacks = [], []
        self.disable_callback = disable_callback
    def __str__(self) -> str: return self.name
    def show_(self, wait=1, destroy=False, built_in_functs=True) -> int:
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
        if not self.disable_callback and self.mouse.new:
            pos = self.mouse.x, self.mouse.y
            v = self.mouse.event, *pos, self.mouse.flags
            for f, p in self.callbacks: f(*v, p)
            for b in self.buttons:
                if b.is_clicked(pos):
                    b.clicked(v)
        if destroy == True: cv2.destroyWindow(self.name)
        elif built_in_functs:
            match wk:
                case 65470 | 269025062: self.move((0, 0)) #f1 | ->
                case 65471 | 269025063: self.move((screen[0], 0)) #f2 | <-
                case 65472 | 269025139: self.fullscreen() #f3 | ⟳
                case 65473: RES.update() # f4
                case 65481 | 27: self.close() # f12 | esc
        return wk
    def move(self, pos) -> None:
        cv2.moveWindow(self.name, *pos)
    def fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
    def setFullscreen(self, fullscreen:bool) -> None:
        self.fullscreen = fullscreen
    def build(self):
        if self.show_(1, False, False) == -1:
            if not self.disable_callback:
                cv2.setMouseCallback(self.name, self.mouse.get)
            return self
        else: raise unreachableImage("An error has occurred while building the image!")
    def show(self, *args, **kwargs) -> int:
        if self.is_opened(): return self.show_(*args, **kwargs)
        else: raise unreachableImage("Maybe you forgot to build the image?")
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
    def line(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a line on the image'''
        cv2.line(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness), lineTypes[lineType%len(lineTypes)])
    def rectangle(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a rectangle on the image'''
        cv2.rectangle(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def polygon(self, pts=[ct_sg(p3, ct), ct_sg(p4, ct), ct_sg(ct, ch)], couleur=COL.black, thickness=1, lineType=0):
        '''Draws a polygon on the image'''
        pts = [[round(i) for i in pt] for pt in pts]
        lineType = lineTypes[lineType%len(lineTypes)]
        couleur = couleur[::-1]; thickness = round(thickness)
        if thickness > 0: cv2.polylines(self.img, [np.array(pts, dtype=np.int32)], True, couleur, thickness, lineType)
        else: cv2.fillPoly(self.img, [np.array(pts, np.int32)], couleur, lineType)
    def circle(self, ct, radius=10, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a circle on the image'''
        cv2.circle(self.img, [round(p) for p in ct], round(radius), colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def ellipse(self, ct, radiuses=[10, 10], colour=COL.black, thickness=1, lineType=0, startAngle=0, endAngle=360, angle=0) -> None:
        '''Draws an ellipse on the image'''
        cv2.ellipse(self.img, [round(p) for p in ct], [round(radius) for radius in radiuses], angle, startAngle, endAngle, colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def save_img(self, path='', fileName=None) -> None:
        '''Saves file'''
        if fileName == None: fileName = self.name
        if path != '': currentWorkingDirPath = os.getcwd(); os.chdir(path)
        cv2.imwrite(fileName, self.img)
        if path != '': os.chdir(currentWorkingDirPath)
    def open_img(self, path) -> None:
        '''Opens local file as image'''
        self.img = cv2.imdecode(np.asarray(bytearray(open(f'{path}', "rb").read()), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    def set_img(self, img) -> None:
        '''Sets the actual image to img'''
        self.img = np.array(img, np.uint8)
    def write_centered(self, text, ct, colour=COL.red, thickness=1, fontSize=1, font=cv2.FONT_HERSHEY_SCRIPT_COMPLEX, lineType=0) -> None:
        '''Write over the image'''
        thickness = round(thickness)
        texts = list(enumerate(str(text).split('\n')))
        x, y = ct[0], ct[1] - round(cv2.getTextSize('Agd', font, fontSize, thickness)[0][1]*(len(texts)-1))
        for i, line in texts:
            tailles = cv2.getTextSize(line, font, fontSize, thickness)
            cv2.putText(self.img, line, (round(x-tailles[0][0]/2), round(y+tailles[1]/2) + i*tailles[0][1]*2), font, fontSize, colour[::-1], thickness, lineTypes[lineType%len(lineTypes)])
    def write(self, text, pt, colour=COL.red, thickness=1, fontSize=1, font=cv2.FONT_HERSHEY_SCRIPT_COMPLEX, lineType=0) -> None:
        cv2.putText(self.img, text, [round(i) for i in pt], font, fontSize, colour[::-1], thickness, lineTypes[lineType%len(lineTypes)])
    def text(self, txt, pt, colour=COL.red, thickness=1, fontSize=1, angle=0, lineType=0, centered=True, help=False, monospace=False, interligne=0):
        Text(text=txt, monospace=monospace).draw(img=self, pt=pt, colour=colour, thickness=thickness, fontSize=fontSize, interligne=interligne, lineType=lineType, angle=angle, centered=centered, help=help)
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
        def __str__(self) -> str:
            return self.name
    def __init__(self, img=new_img(), frames=[], name="Layout") -> None:
        self.name, self.img, self.frames = name, img.copy(), frames
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
