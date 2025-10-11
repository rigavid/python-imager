from PIL import Image, ImageDraw, ImageFont
import os, copy, numpy as np, random as rd
try: from pyimager.__vars__ import *
except: from __vars__ import *
import cv2

# Mandatory for Fedora (Wayland?), works on Windows too # TEST see if it works on other distros
try: os.environ["XDG_SESSION_TYPE"] = "xcb"
except: pass

class unreachableImage(Exception): pass
def fusionImages(img, base_img, pos=[0, 0]):
    '''Place an image over another'''
    x_offset, y_offset = pos = [round(v) for v in pos]
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
def new_img(dimensions=None, background=COL.white, name="NewImg"):
    return image(name, image.new_image(dimensions=dimensions if dimensions!=None else RES.resolution, background=background))
class image:
    class mouse:
        new = False
        event = x = y = flags = pos = None
        def get(event, x, y, flags, _):
            image.mouse.new = True
            image.mouse.event = event
            image.mouse.x, image.mouse.y = x, y
            image.mouse.flags = flags
            image.mouse.pos = x, y
            return event, x, y, flags
    def setMouseCallback(self, funct, params=None) -> None:
        '''event, x, y, flags, params -> None'''
        self.callbacks.append([funct, params])
    class trackbar_:
        def defImg(self, img) -> None: self.img = img
        def __init__(self, name="TrackBar", coos=[[100, 200], [500, 300]], min=0, max=100, val=0, col1=COL.red, col2=COL.darkRed, col3=COL.green, font=None, thickness=3, lineType=2, fontSize=1) -> None:
            self.name, self.coos = name, coos
            self.value = val if min<=val and max>=val else min if val<min else max
            self.range = (min, max)
            self.changing = False
            self.col1, self.col2, self.col3 = col1, col2, col3
            self.tk, self.lt, self.fs, self.font = thickness, lineType, fontSize, font
        def is_clicked(self, coos) -> bool: return clicked_in(coos, self.coos)
        def pnts(self, g, d, i, y, n) -> tuple:
            return (coosCircle(coosCircle(g, dist(g, d)*(i/diff(*self.range)), 0), y/n/2, a) for a in (90, 270))
        def draw(self) -> None: ## TODO Write value, minimum and maximum somewhere
            self.img.rectangle(*self.coos, self.col1, 0, self.lt)
            self.img.rectangle(*self.coos, self.col2, self.tk, self.lt)
            p1, p4 = self.coos
            x, y = diff(p4[0], p1[0]), diff(p4[1], p1[1])
            dx = x/50
            self.img.text(self.name, (p1[0]+dx, p1[1]+y/2), self.col2, self.tk, self.fs, police=self.police, anchor="lm")
            X, Y = self.img.textSize(self.name, self.police, fontSize=self.fs)
            g, d = (p1[0]+X+dx*2, p1[1]+y/2), (p4[0]-dx, p4[1]-y/2)
            self.img.line(g, d, self.col2, self.tk, self.lt)
            m = diff(*self.range)
            for n, i in enumerate(range(0, m+1, 5)):
                self.img.line(*self.pnts(g, d, i, y, 2 if n%5==0 else 4), self.col2, self.tk, self.lt)
            self.img.line(*self.pnts(g, d, self.value-self.range[0], y, 3), self.col3, self.tk, self.lt)
            self.scale = g[0], d[0]
        def get(self) -> number: return self.value
    def trackbar(self, *args, **kwargs) -> trackbar_:
        trkb = self.trackbar_(*args, **kwargs)
        trkb.defImg(self)
        trkb.draw()
        self.trackbars.append(trkb)
        return trkb
    def remove_trackbar(self, trkb) -> trackbar_ | int:
        try: return self.trackbars.pop(self.trackbars.index(trkb))
        except: return -1
    class button_:
        def __init__(self, name="Button", coos=[[100,100], [300, 200]], font=None, col1=COL.red, col2=COL.darkRed, thickness=3, lineType=2, fontSize=1) -> None:
            self.name, self.coos = name, coos
            self.col1, self.col2 = col1, col2
            self.tk, self.lt, self.fs, self.font = thickness, lineType, fontSize, font
            self.functs = []
        def defImg(self, img) -> None: self.img = img
        def draw(self) -> None:
            self.img.rectangle(*self.coos, self.col1, 0, 2)
            self.img.rectangle(*self.coos, self.col2, self.tk, 2)
            self.img.text(self.name, ct_sg(*self.coos), self.col2, self.tk, self.fs, anchor="mm")
        def on_click(self, funct, params=None) -> None:
            '''To add a function to execute when clicked'''
            self.functs.append([funct, params])
        def clicked(self, vars_get) -> None:
            '''Execute each function'''
            for f, p in self.functs: f(*vars_get, p)
        def is_clicked(self, coos) -> bool: return clicked_in(coos, self.coos)
    def button(self, *args, **kwargs) -> button_:
        bttn = self.button_(*args, **kwargs)
        bttn.defImg(self)
        bttn.draw()
        self.buttons.append(bttn)
        return bttn
    def remove_button(self, bttn) -> button_ | int:
        try: return self.buttons.pop(self.buttons.index(bttn))
        except: return -1
    ################################################################
    def new_image(self=None, dimensions=RES.resolution, background=COL.white) -> np.array:
        '''New image'''
        return np.full([round(v) for v in dimensions[::-1]]+[3], background[::-1], np.uint8)
    def __init__(self, name="python-image", img=None, disable_callback=False) -> None:
        self.img = np.array(self.new_image() if type(img) == type(None) else img.img if type(img) == image else img)
        self.name, self.fullscreen = name, False
        self.buttons, self.trackbars, self.callbacks = [], [], []
        self.disable_callback = disable_callback
        self.new_res = False
    def __str__(self) -> str: return self.name
    def copy(self):
        '''Returns a copy of itself'''
        return image(self.nom, copy.deepcopy(self.img))
    def size(self, rev=False) -> [int, int]:
        '''Returns image's size (reverse True means [y,x] whereas False means [x,y])'''
        return [len(self.img[0]), len(self.img)][::-1 if rev else 1]
    def build(self):
        if self.show_(1, False, False) == -1:
            if not self.disable_callback:
                cv2.setMouseCallback(self.name, self.mouse.get)
            return self
        else: raise unreachableImage("An error has occurred while building the image!")
    def close(self) -> None:
        '''Closes window'''
        if not self.is_closed(): cv2.destroyWindow(self.name)
    def open_img(self, path) -> None:
        '''Opens local file as image'''
        self.img = cv2.imdecode(np.asarray(bytearray(open(f'{path}', "rb").read()), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    def save_img(self, path='', fileName=None) -> None:
        '''Saves file'''
        if fileName == None: fileName = self.name
        if path != '': currentWorkingDirPath = os.getcwd(); os.chdir(path)
        cv2.imwrite(fileName, self.img)
        if path != '': os.chdir(currentWorkingDirPath)
    def set_img(self, img) -> None:
        '''Sets the actual image to img'''
        self.img = np.array(img, np.uint8)
    def show_(self, wait=1, destroy=False, built_in_functs=True, QtGui=False) -> int:
        '''Show image in a window'''
        props = cv2.WND_PROP_FULLSCREEN | (cv2.WINDOW_GUI_EXPANDED if QtGui else cv2.WINDOW_GUI_NORMAL)
        cv2.namedWindow(self.name, props)
        if self.fullscreen:
            cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty(self.name, cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_KEEPRATIO)
        else: cv2.setWindowProperty(self.name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_KEEPRATIO)
        cv2.imshow(self.name, cv2.resize(np.array(self.img, np.uint8), RES.resolution))
        wk = cv2.waitKeyEx(wait)
        if not self.disable_callback and self.mouse.new:
            self.mouse.new = False
            pos = self.mouse.x, self.mouse.y
            v = self.mouse.event, *pos, self.mouse.flags
            for f, p in self.callbacks: f(*v, p)
            for b in self.buttons:
                if b.is_clicked(pos):
                    b.clicked(v)
            for t in self.trackbars:
                if v[0] == cv2.EVENT_LBUTTONDOWN:
                    if not t.changing and t.is_clicked(pos): t.changing = True
                elif v[0] == cv2.EVENT_MOUSEMOVE and t.changing:
                    g, d, x = *t.scale, v[1]
                    t.value = t.range[0] if x<=g else t.range[1] if x>=d else t.range[0]+diff(*t.range)/diff(g, d)*diff(g, x)
                    print(g, d, x, t.value)
                    t.draw()
                elif v[0] == cv2.EVENT_LBUTTONUP:
                    if t.changing:
                        g, d, x = *t.scale, v[1]
                        t.value = t.range[0] if x<=g else t.range[1] if x>=d else t.range[0]+diff(*t.range)/diff(g, d)*diff(g, x)
                        t.changing = False
                        t.draw()
        if destroy == True: cv2.destroyWindow(self.name)
        elif built_in_functs:
            match wk:
                case 65470: self.move((0, 0)) #f1
                case 65471: self.move((screen[0], 0)) #f2
                case 65472: self.toggleFullscreen() #f3
                case 65473:
                    RES.update() # f4
                    self.new_res = True
                case 65481 | 27: self.close() # f12 | esc
        return wk
    def show(self, *args, **kwargs) -> int:
        if self.is_opened(): return self.show_(*args, **kwargs)
        else: raise unreachableImage("Maybe you forgot to build the image?")
    def move(self, pos) -> None:
        cv2.moveWindow(self.name, *pos)
    def toggleFullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
    def setFullscreen(self, fullscreen:bool) -> None:
        self.fullscreen = fullscreen
    def is_closed(self) -> bool:
        '''Detect if the window is currently closed'''
        try: return cv2.getWindowProperty(self.name, cv2.WND_PROP_VISIBLE) < 1
        except: return True
    def is_opened(self) -> bool:
        '''Detect if the window is currently opened'''
        return not self.is_closed()
    def line(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a line on the image'''
        cv2.line(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness), lineTypes[lineType%len(lineTypes)])
    def rectangle(self, p1, p2, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a rectangle on the image'''
        cv2.rectangle(self.img, [round(p) for p in p1], [round(p) for p in p2], colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def circle(self, ct, radius=10, colour=COL.black, thickness=1, lineType=0) -> None:
        '''Draws a circle on the image'''
        cv2.circle(self.img, [round(p) for p in ct], round(radius), colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def ellipse(self, ct, radiuses=[10, 10], colour=COL.black, thickness=1, lineType=0, startAngle=0, endAngle=360, angle=0) -> None:
        '''Draws an ellipse on the image'''
        cv2.ellipse(self.img, [round(p) for p in ct], [round(radius) for radius in radiuses], angle, startAngle, endAngle, colour[::-1], round(thickness) if thickness != 0 else -1, lineTypes[lineType%len(lineTypes)])
    def polygon(self, pts=[ct_sg(p3, ct), ct_sg(p4, ct), ct_sg(ct, ch)], couleur=COL.black, thickness=1, lineType=0):
        '''Draws a polygon on the image'''
        pts = [[round(i) for i in pt] for pt in pts]
        lineType = lineTypes[lineType%len(lineTypes)]
        couleur = couleur[::-1]; thickness = round(thickness)
        if thickness > 0: cv2.polylines(self.img, [np.array(pts, dtype=np.int32)], True, couleur, thickness, lineType)
        else: cv2.fillPoly(self.img, [np.array(pts, np.int32)], couleur, lineType)
    def textSize(self, text, police="default", thickness=1, fontSize=1) -> tuple:
        if police in ["", None]: police = "default"
        try: font = ImageFont.truetype(f"{f"{fonts_path}/"if police=="default"else""}{police}.ttf", fontSize)
        except OSError as e:
            print(f"Couldn't load font: <{police}>")
            raise e
        xa, ya, xb, yb = ImageDraw.Draw(Image.fromarray(self.img)).multiline_textbbox((0,0), text, font)
        return (round(diff(xa, xb)),round(diff(ya, yb)))
    def text(self, text, pt, col=COL.red, thickness=1, fontSize=1, angle=0, anchor="mm", police="default") -> None:
        """
        The anchor is a string 'XY'
        For X: use l for left, m for middle and r for.
        For Y: use t for top, m for middle and b for bottom.
        For more information, cf. https://hugovk-pillow.readthedocs.io/en/stable/handbook/text-anchors.html (20251011)
        """
        if police in ["", None]: police = "default"
        try: font = ImageFont.truetype(f"{f"{fonts_path}/"if police=="default"else""}{police}.ttf", fontSize)
        except OSError as e:
            print(f"Couldn't load font: <{police}>")
            raise e
        xa, ya, xb, yb = ImageDraw.Draw(img:=Image.fromarray(self.img)).multiline_textbbox((0,0), text, font, anchor)
        mask_size = (width:=round(diff(xa, xb)+fontSize*10), height:=round(diff(ya, yb)+fontSize*10))
        width = height = max(mask_size)
        mask_size = (width, height)
        ImageDraw.Draw(im:=Image.new('RGBA', mask_size, (0,0,0,0))).text((width/2, height/2), text, font=font, fill=tuple(col), anchor=anchor)
        im = im.rotate(-angle)
        img.paste(im, [round(pt[0]-width/2), round(pt[1]-height/2)], im)
        self.img = np.array(img)
    def write(self, text, pt, font, colour=COL.red, thickness=1, fontSize=1, lineType=0) -> None:
        cv2.putText(self.img, text, [round(i) for i in pt], font, fontSize, colour[::-1], thickness, lineTypes[lineType%len(lineTypes)])
    def write_centered(self, text, ct, font, colour=COL.red, thickness=1, fontSize=1, lineType=0) -> None:
        '''Write over the image'''
        thickness = round(thickness)
        texts = list(enumerate(str(text).split('\n')))
        x, y = ct[0], ct[1] - round(cv2.getTextSize('Agd', font, fontSize, thickness)[0][1]*(len(texts)-1))
        for i, line in texts:
            tailles = cv2.getTextSize(line, font, fontSize, thickness)
            cv2.putText(self.img, line, (round(x-tailles[0][0]/2), round(y+tailles[1]/2) + i*tailles[0][1]*2), font, fontSize, colour[::-1], thickness, lineTypes[lineType%len(lineTypes)])
## TODO Check that layouts still works and update it if necessary ##
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
if __name__ == "__main__":
    img = image().build()
    img.show(0)