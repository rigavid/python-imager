try: from pyimager.main import *
except: from main import *

def draw_char(img, char, pts, colour=COL.red, thickness=1, lineType=0, angle=0):
    ct = ct_cr(*pts)
    p1, p2, p3, p4 = [pt_sg(p, ct, 5) for p in pts]
    match char:
        case "00":
            pt, rs = pt_sg(ct, ct_sg(p1, p2), 3), [dist(ct, p1)*0.3, dist(ct, p1)*0.4]
            img.ellipse(pt, rs, colour, thickness, lineType, 200, 450, angle)
            pt1 = coosEllipse(pt, rs, 90)
            pt2 = coosCircle(pt1, dist(p1, p3)/10, 90)
            p1, p2, p3, p4 = [pt_sg(p, ct, 10) for p in pts]
            LINES = [p1, p3], [p1, p2], [p2, p4], [p3, p4], [pt1, pt2]
            for p1, p2 in LINES: img.line(p1, p2, colour, thickness, lineType)