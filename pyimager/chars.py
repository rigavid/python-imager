try: from pyimager.main import *
except: from main import *

def draw_char(img, char, pts, colour=COL.red, fontSize=1, thickness=1, lineType=0, angle=0):
    col, tk, lt, an = colour, thickness, lineType, angle
    ct = ct_cr(*pts)
    p1, p2, p3, p4 = ps = [coosCircle(p, fontSize, a) for p,a in zip(pts, (45, 135, 315, 225))]
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    LINES = []
    match char:
        case "00": ## Unknown char !
            pt, rs = pt_sg(ct, ct_sg(p1, p2), 3), [dist(ct, p1)*0.2, dist(ct, p1)*0.3]
            pt1 = coosEllipse(pt, rs, 90); pt2, pt3 = coosCircle(pt1, dist(p1, p3)/10, 90), coosCircle(pt1, dist(p1, p3)/5, 90)
            LINES = [[ch, cd], [cd, cb], [cb, cg], [cg, ch], [pt1, pt2]]
            LINES.extend([pts[(0,1,3,2)[i]],pts[(0,1,3,2)[(i+1)%4]]]for i in range(4))
            img.ellipse(pt, rs, col, tk, lt, 200, 450, an)
            img.circle(pt3, tk, col, 0, lt)
        case "A00":
            p1, p2, p3, p4 = [pt_sg(p, ct, 5) for p in pts]
            LINES = [[p3, ch], [ch, p4], [ct_sg(p3, ch), ct_sg(ch, p4)]] ## A
        case "A01": ## B
            LINES = [[p1, p3], [p3, cb], [cg, ct], [p1, ch]]
            pt1, pt2 = ct_sg(ct, ch), ct_sg(ct, cb)
            img.ellipse(pt1, [dist(ch, p2)*0.8, dist(pt1, ch)], col, tk, lt, 270, 450, an)
            img.ellipse(pt2, [dist(ct, cd), dist(pt2, cb)], col, tk, lt, 270, 450, an)
        case "A02": ## C
            p = ct_sg(ct, cd)
            img.ellipse(p, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 50, 300, an)
        case "A03": ## D
            LINES = [[p1, p3], [p3, cb], [p1, ch]]
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 270, 450, an)









    #################################################
    for a, b in LINES: img.line(a, b, col, tk, lt) ##
    return ##########################################