try:
    from pythonImager.resolution import resolution as RES
    from pythonImager.colors import colour as COL
    import pythonImager.terminal_colors as TCOL
    from pythonImager.calculs import *
except:
    from resolution import resolution as RES
    from colors import colour as COL
    import terminal_colors as TCOL
    from calculs import *
from cv2 import LINE_4, LINE_8, LINE_AA


long, haut = screen = RES.resolution
hg, hd, bg, bd = [0, 0], [long, 0], [0, haut], [long, haut]
ct, p1, p2, p3, p4 = [round(long/2), round(haut/2)], [round((long-haut)/2), 0], [round((long-haut)/2)+haut, 0], [round((long-haut)/2), haut], [round((long-haut)/2)+haut, haut]
cg, cd, ch, cb = ct_sg(p1, p3), ct_sg(p2, p4), ct_sg(p1, p2), ct_sg(p3, p4)
lineTypes = [LINE_4, LINE_8, LINE_AA]
fonts_path = "/".join(i for i in __file__.split("/")[:-1])+"/fonts/"