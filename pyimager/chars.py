try: from pyimager.main import *
except: from main import *

def draw_char(img, char, pts, colour=COL.red, fontSize=1, thickness=1, lineType=0, angle=0, help=False):
    if help:
        img.circle(pts[-1], 4, COL.green, 0)
        for p in pts[:-1:]: img.circle(p, 3, COL.red, 0)
        img.write(char, pts[0])
    col, fs, tk, lt, an = colour, fontSize, thickness, lineType, angle
    ct = ct_cr(*pts)
    p1, p2, p3, p4 = ps = [coosCircle(p, fontSize, a+an) for p,a in zip(pts, (45, 135, 315, 225))]
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    LINES = []
    match char:
        case "00": ## Unknown char !
            pt, rs = pt_sg(ct, ct_sg(p1, p2), 3), (dist(ct, p1)*0.2, dist(ct, p1)*0.3)
            pt1 = coosEllipse(pt, rs, 90+an)
            pt2, pt3 = coosCircle(pt1, dist(p1, p3)/10, 90+an), coosCircle(pt1, dist(p1, p3)/5, 90+an)
            LINES = [[ch, cd], [cd, cb], [cb, cg], [cg, ch], [pt1, pt2]] + [[pts[(0,1,3,2)[i]], pts[(0,1,3,2)[(i+1)%4]]] for i in range(4)]
            img.ellipse(pt, rs, col, tk, lt, 200, 450, an)
            img.circle(pt3, tk, col, 0, lt)
        case "E2": ## `
            LINES = [[pt_sg(*pts[:2:], 2), pt_sg(*ps[:2:], 1, 2)]]
        case "E3": ## ´
            LINES = [[pt_sg(*pts[:2:], 1, 2), pt_sg(*ps[:2:], 2)]]
        case "E4": ## ^
            LINES = [[ct_sg(*pts[:2:]), pt_sg(*ps[:2:], 4)], [ct_sg(*pts[:2:]), pt_sg(*ps[:2:], 1, 4)]]
        case "A00": ## A
            LINES = [[p3, ch], [ch, p4], [ct_sg(p3, ch), ct_sg(ch, p4)]]
        case "A01": ## B
            LINES = [[p1, p3], [p3, cb], [cg, ct], [p1, ch]]
            pt1, pt2 = ct_sg(ct, ch), ct_sg(ct, cb)
            img.ellipse(pt1, (dist(ch, p2)*0.8, dist(pt1, ch)), col, tk, lt, 270, 450, an)
            img.ellipse(pt2, (dist(ct, cd), dist(pt2, cb)), col, tk, lt, 270, 450, an)
        case "A02": ## C
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 50, 300, an)
        case "A03": ## D
            LINES = [[p1, p3], [p3, cb], [p1, ch]]
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 270, 450, an)
        case "A04": ## E
            LINES = [[p1, p3], [cg, ct_sg(ct, cd)], [p3, p4], [p1, p2]]
        case "A05": ## F
            LINES = [[p1, p3], [cg, ct_sg(ct, cd)], [p1, p2]]
        case "A06": ## G
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 0, 300, an)
            LINES = [[ct, cd]]
        case "A07": ## H
            LINES = [[p1, p3], [p2, p4], [cg, cd]]
        case "A08": ## I
            LINES = [[p1, p2], [p3, p4], [ch, cb]]
        case "A09": ## J
            p, pt2 = ct_sg(cd, p4), ct_sg(ct, cb)
            LINES = [[ct_sg(p1, ch), p2], [p2, p]]
            img.ellipse(pt2, (dist(p, pt2), dist(pt2, cb)), col, tk, lt, 0, 135, an)
        case "A10": ## K
            p = pt_sg(cg, p3, 3)
            LINES = [[p1, p3], [p, p2], [pt_sg(p, p2, 2), p4]]
        case "A11": ## L
            LINES = [[p1, p3], [p3, p4]]
        case "A12": ## M
            LINES = [[p1, p3], [p1, pt_sg(ct, cb, 3)], [pt_sg(ct, cb, 3), p2], [p2, p4]]
        case "A13": ## N
            LINES = [[p1, p3], [p1, p4], [p2, p4]]
        case "A14": ## O
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, angle=an)
        case "A15": ## P
            LINES = [[p1, p3], [cg, ct], [p1, ch]]
            pt1 = ct_sg(ct, ch)
            img.ellipse(pt1, (dist(ch, p2)*0.8, dist(pt1, ch)), col, tk, lt, 270, 450, an)
        case "A16": ## Q
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, angle=an)
            LINES = [[pt_sg(cb, ct, 4), p4]]
        case "A17": ## R
            LINES = [[p1, p3], [cg, ct], [p1, ch], [ct, p4]]
            pt1 = ct_sg(ct, ch)
            img.ellipse(pt1, [dist(ch, p2)*0.8, dist(pt1, ch)], col, tk, lt, 270, 450, an)
        case "A18": ## S ## FIXME
            pt1, pt2 = ct_sg(ct, ch), ct_sg(ct, cb)
            img.ellipse(pt1, (dist(ch, p2)*0.8, dist(pt1, ch)), col, tk, lt, 90, 300, an)
            img.ellipse(pt2, (dist(cb, p4)*0.8, dist(pt2, cb)), col, tk, lt, -90, 130, an)
        case "A19": ## T
            LINES = [[p1, p2], [ch, cb]]
        case "A20": ## U
            LINES = [[p1, ct_sg(cg, p3)], [p2, ct_sg(cd, p4)]]
            img.ellipse(ct_sg(cg, p4), (dist(ct, cd), dist(ct, cb)/2), col, tk, lt, 0, 180, an)
        case "A21": ## V
            LINES = [[p1, cb], [p2, cb]]
        case "A22": ## W
            cbg, cbd = ct_sg(p3, cb), ct_sg(p4, cb)
            LINES = [[p1, cbg], [ct, cbg], [ct, cbd], [p2, cbd]]
        case "A23": ## X
            LINES = [[p1, p4], [p2, p3]]
        case "A24": ## Y
            LINES = [[p1, ct], [p2, ct], [ct, cb]]
        case "A25": ## Z
            LINES = [[p1, p2], [p2, p3], [p3, p4]]








    #################################################
        case _: draw_char(img, "00", pts, col, fs, tk, lt, an, False)
    for a, b in LINES: img.line(a, b, col, tk, lt) ##
    return ##########################################
def draw_diacr(img, char, *args, **kwargs):
    match char:
        case "40": char = "E2"
        case "41": char = "E3"
        case "42": char = "E4"
        case "46": char = "E5"
        case _: char = "00"
    draw_char(img, char, *args, **kwargs)