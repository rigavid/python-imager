try: from pyimager.main import *
except: from main import *

class ANG:
    def ang_h(a:float) -> float: ## HM
        rad = math.radians(a)
        sin, acos = math.sin(rad), math.acos(-math.cos(rad))
        angle = math.degrees(-acos if sin<0 else acos)
        return angle
    def ang_v(a:float) -> float: ## VM
        rad = math.radians(a)
        sin, acos = -math.sin(rad), math.acos(math.cos(rad))
        angle = math.degrees(-acos if sin<0 else acos)
        return angle
    def angHV(a:float) -> float: ## HM+VM
        rad = math.radians(a)
        sin, acos = -math.sin(rad), math.acos(-math.cos(rad))
        angle = math.degrees(-acos if sin<0 else acos)
        return angle

def get_coos(ps):
    p1, p2, p3, p4, ct = *ps, ct_cr(*ps)
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    cth, ctb, ctg, ctd = ct_sg(ct, ch), ct_sg(ct, cb), ct_sg(ct, cg), ct_sg(ct, cd)
    ct1, ct2, ct3, ct4 = ct_sg(ct, p1), ct_sg(ct, p2), ct_sg(ct, p3), ct_sg(ct, p4)
    phg, phd, pbg, pbd = ct_sg(p1, ch), ct_sg(p2, ch), ct_sg(p3, cb), ct_sg(p4, cb)
    pgh, pdh, pgb, pdb = ct_sg(p1, cg), ct_sg(p2, cd), ct_sg(p3, cg), ct_sg(p4, cd)
    return ct,p1,p2,p3,p4,ch,cb,cg,cd,cth,ctb,ctg,ctd,ct1,ct2,ct3,ct4,phg,phd,pbg,pbd,pgh,pdh,pgb,pdb

def draw_char(img, char, pts, colour=COL.red, fontSize=1, thickness=1, lineType=0, angle=0, help=False):
    ## VARS ##
    points = copy.deepcopy(pts)
    col, fs, tk, lt, an, sty = colour, fontSize, thickness, lineType, angle%360, ""
    ps = [coosCircle(p, fs, a+an) for p, a in zip(pts, (45, 135, 315, 225))]
    LINES, ang = [], lambda a: a
    ## Modif vars selon style ##
    if not (type(char)==str or not ":" in str(char)): ### Adapter les variables selon le style à appliquer
        lc = col
        c, s = str(char).split(":")[0], str(char).split(":")[1::]
        sty = ":"+":".join(i for i in s)
        if "OL" in s: LINES += [[ct_sg(pts[0], pts[2]), ct_sg(pts[1], pts[3])]]
        if "UL" in s: LINES += [[pts[2], pts[3]]]
        if "TL" in s: LINES += [[pts[0], pts[1]]]
        if "TN" in s: tk = 1 if tk <= 1 else tk/2
        if "BD" in s: tk *= 2
        if "VM" in s and "HM" in s:
            ps, pts, ang = ps[::-1], pts[::-1], ANG.angHV
        elif "VM" in s:
            ang, o = ANG.ang_v, (2,3,0,1)
            ps, pts = [ps[i] for i in o], [pts[i] for i in o]
        elif "HM" in s:
            ang, o = ANG.ang_h, (1,0,3,2)
            ps, pts = [ps[i] for i in o], [pts[i] for i in o]
        if "IT" in s:
            ps[:2:] = (coosCircle(p, fontSize, ang(an)) for p in (ps[0], ps[1]))
            an += (angleInterPoints(ps[1], ps[-1])-90)/2
        if "CI" in s:
            ps[:2:] = (coosCircle(p, fontSize, ang(an+180)) for p in (ps[0], ps[1]))
            an += (angleInterPoints(ps[1], ps[-1])-90)/2
        for st in (i for i in s if len(i) == 10):
            if   "BG" in st: img.polygon([pts[i] for i in (0, 1, 3, 2)], COL.new(st[3:-1:]), 0)
            elif "FG" in st: col = COL.new(st[3:-1:])
            elif "LS" in st: lc = COL.new(st[3:-1:])
        for a, b in LINES: img.line(a, b, lc, tk*1.5, lt)
        LINES = []
    ct,p1,p2,p3,p4,ch,cb,cg,cd,cth,ctb,ctg,ctd,ct1,ct2,ct3,ct4,phg,phd,pbg,pbd,pgh,pdh,pgb,pdb = get_coos(ps)
    D = dist(pts[0], p1)/2
    match char:
        ## "Control" chars #####################################
        case "00": ## Unknown char !
            pt, rs = pt_sg(ct, ch, 3), (dist(ct, p1)*0.2, dist(ct, p1)*0.3)
            pt1 = coosEllipse(pt, rs, 90, an)
            pt2, pt3 = coosCircle(pt1, dist(p1, p3)/10, 90+an), coosCircle(pt1, dist(p1, p3)/5, 90+an)
            LINES += [[ch, cd], [cd, cb], [cb, cg], [cg, ch], [pt1, pt2]] + [[pts[(0,1,3,2)[i]], pts[(0,1,3,2)[(i+1)%4]]] for i in range(4)]
            img.ellipse(pt, rs, col, tk, lt, 200, 450, an)
            img.circle(pt3, tk, col, 0, lt)
        case "06": ## Full char
            img.polygon([*pts[:2:], *pts[:1:-1]], col, 0, lt)
        ## Diacritiques suscrits ###############################
        case "40": # `
            if char.upper:
                pts = pt_sg(*pts[:2:], 2), pt_sg(p2, p1, 2)
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in pts]]
            else: LINES += [[pt_sg(ct1, ct2, 2), pt_sg(ct_sg(cd, pdh), ct_sg(cg, pgh), 2)]]
        case "41": # ´
            if char.upper:
                pts = pt_sg(*pts[1::-1], 2), pt_sg(p1, p2, 2)
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in pts]]
            else: LINES += [[pt_sg(ct2, ct1, 2), pt_sg(ct_sg(cg, pgh), ct_sg(cd, pdh), 2)]]
        case "42": # ^
            if char.upper:
                ls = [[pt_sg(p2, p1, 2), ct_sg(*pts[1::-1])], [ct_sg(*pts[1::-1]), pt_sg(p1, p2, 2)]]
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in l] for l in ls]
            else: LINES += [[ct_sg(cg, cth), cth], [cth, ct_sg(cd, cth)]]
        case "43": # ˇ
            if char.upper:
                ls = [[pt_sg(*pts[1::-1], 2), ch], [ch, pt_sg(*pts[:2:], 2)]]
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in l] for l in ls]
            else: LINES += [[ct1, ct_sg(cth, ct)], [ct_sg(cth, ct), ct2]]
        case "44": # ̏
            if char.upper:
                ls = [[ch, pt_sg(*pts[:2:], 3, 2)], [ct_sg(phd, ch), pt_sg(*pts[:2:], 3, 3)]]
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in l] for l in ls]
            else: LINES += [[ct1, ct_sg(cth, ct)], [cth, ct_sg(ctd, ct2)]]
        case "45": # ̋
            if char.upper:
                ls = [[ch, pt_sg(*pts[1::-1], 3, 2)], [ct_sg(phg, ch), pt_sg(*pts[1::-1], 3, 3)]]
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in l] for l in ls]
            else: LINES += [[ct2, ct_sg(cth, ct)], [cth, ct_sg(ctg, ct1)]]
        case "46": # ¨
            if char.upper: pts = [coosCircle(p, D/2, ang(-90)+an) for p in (pt_sg(*pts[:2:], 2), pt_sg(*pts[1::-1], 2))]
            else: pts = (pt_sg(ct1, ct, 2), pt_sg(ct2, ct, 2))
            for p in pts: img.circle(p, fontSize*0.1*tk, col, -tk, lt)
        case "47": # ̇
            if char.upper: img.circle(coosCircle(ct_sg(*pts[:2:]), D/2, ang(-90)+an), fontSize*0.1*tk, col, -tk, lt)
            else: img.circle(ct_sg(ct1, ctd), fontSize*0.1*tk, col, -tk, lt)
        case "48": # ̆
            r = (fontSize*0.4 for _ in "00")
            a = [ang(0), ang(180)]
            if "VM" in sty:
                an+=180
                if not "HM" in sty: a[1] += 360
            if char.upper: img.ellipse(coosCircle(ct_sg(*pts[:2:]), D/2, ang(-90)+an), r, col, tk, lt, *a, an)
            else: img.ellipse(pt_sg(cth, ct, 2), r, col, tk, lt, *a, an)
        case "49": # ¯
            if char.upper:
                pts = [pt_sg(*pts[1::-1], 2), pt_sg(*pts[:2:], 2)]
                LINES += [[coosCircle(p, D/2, ang(-90)+an) for p in pts]]
            else: LINES += [[ct_sg(ct1, ctg), ct_sg(ct2, ctd)]]
        case "50": # ~
            if char.upper:
                pt1, pt2 = pt_sg(*pts[:2:], 3, 2), pt_sg(*pts[1::-1], 3, 2)
                r = (dist(pt1, ct_sg(*pts[:2:])), dist(ct_sg(*pts[:2:]), ch)/3)
                pt1, pt2 = (coosCircle(p, D/2, ang(-90)+an) for p in (pt1, pt2))
            else:
                pt1, pt2 = ct_sg(cth, ctg), ct_sg(cth, ctd)
                r = (dist(pt1, ct_sg(cth, ct)), dist(ct_sg(*pts[:2:]), ch)/3)
            a = 360 if "VM" in sty else 0
            if "HM" in sty: an+=180
            img.ellipse(pt1, r, col, tk, lt, ang(180)+a, ang(360), an)
            img.ellipse(pt2, r, col, tk, lt, ang(0), ang(180), an)
        case "51": # '
            if char.upper:
                pts = ct_sg(*pts[:2:]), pt_sg(ch, ct_sg(*pts[:2:]), 2)
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in pts]]
            else: LINES += [[cth, ct_sg(cth, ct)]]
        case "52": # "
            if char.upper:
                pt1, pt2 = pt_sg(*pts[:2:], 5, 4), pt_sg(*pts[:2:], 4, 5)
                d = dist(pt1, pt_sg(ch, ct_sg(*pts[:2:]), 2))
                ls = [[pt1, coosCircle(pt1, d, ang(90)+an)], [pt2, coosCircle(pt2, d, ang(90)+an)]]
                LINES += [[coosCircle(p, D, ang(-90)+an) for p in l] for l in ls]
            else:
                d, pt1, pt2 = dist(cth, ct_sg(cth, ct)), ct_sg(cth, ct1), ct_sg(cth, ct2)
                LINES += [[pt1, coosCircle(pt1, d, ang(90)+an)], [pt2, coosCircle(pt2, d, ang(90)+an)]]
        case "53": # °
            if char.upper: img.circle(ct_sg(*pts[:2:]), fontSize*0.4, col, tk, lt)
            else: img.circle(pt_sg(cth, ct, 2), fontSize*0.4, col, tk, lt)
        case "54": # ̉
            a, r = [ang(-120), ang(90)], (fontSize*0.4, fontSize*0.4)
            if char.upper: img.ellipse(coosCircle(ct_sg(*pts[:2:]), D/2, ang(-90)+an), r, col, tk, lt, *a, an)
            else: img.ellipse(pt_sg(cth, ct, 2), r, col, tk, lt, *a, an)
        ## Diacritiques souscrits ##############################
        case "60": # Cédille
            LINES += [[ct_sg(ct4, cb), pt_sg(*pts[2::], 2)]]
        case "61": # Ogonyek
            LINES += [[ct_sg(ct3, cb), pt_sg(*pts[:1:-1], 2)]]
        case "62": # Vertical line below
            d = dist(p4, pts[-1])
            LINES += [[coosCircle(cb, d/2, ang(90)+an), coosCircle(cb, d*1.25, ang(90)+an)]]
        case "63": # Dot below
            img.circle(ct_sg(*pts[2::]), fontSize*0.1*tk, col, -tk, lt)
        ## Diacritiques inscrits ###############################
        case "80": # ̛
            a, r = [ang(-120), ang(90)], (fontSize*0.4, fontSize*0.4)
            if char.upper: img.ellipse(p2, r, col, tk, lt, *a, an)
            else: img.ellipse(cd, r, col, tk, lt, *a, an)
        ## Symbols #############################################
        case "A0": ## 0
            r = (dist(ct, ct_sg(cd, ctd)), dist(ct, ch))
            img.ellipse(ct, r, col, tk, lt, angle=an)
            LINES += [[coosEllipse(ct, r, ang(140), an), coosEllipse(ct, r, ang(320), an)]]
        case "A1": ## 1
            LINES += [[ct_sg(ct1, pgh), ch], [ch, cb], [p3, p4]]
        case "A2": ## 2
            r = (dist(ct, cd), dist(cth, ch))
            a1 = [ang(a) for a in (400, 210)]
            if "HM" in sty: a1 = [a%360 for a in a1]
            img.ellipse(cth, r, col, tk, lt, *a1, an)
            LINES += [[coosEllipse(cth, r, a1[0], an), p3], [p3, p4]]
        case "A3": ## 3
            a1, a2 = (ang(220), ang(450)), (ang(270), ang(510))
            if "HM" in sty: a1, a2 = [a%360 for a in a1], [a%360 for a in a2]
            img.ellipse(cth, (dist(ct, cd), dist(cth, ch)), col, tk, lt, *a1, an)
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, *a2, an)
        case "A4": ## 4
            LINES += [[phd, ct_sg(cg, pgb)], [ct_sg(cg, pgb), ct_sg(cd, pdb)], [phd, pbd]]
        case "A5": ## 5
            p, pe = pt_sg(p1, phg, 3), pt_sg(ct, cb, 3, 2)
            LINES += [[p, p2], [p, cg]]
            a1, a2, a3 = (ang(180), ang(270)), (ang(-90), ang(90)), (ang(90), ang(180))
            if "HM" in sty:
                if not "VM" in sty: a3 = [a%360 for a in a3]
                a2 = [a%360 for a in a2]
            if "VM" in sty: a1 = [a%360 for a in a1]
            img.ellipse(ct, (dist(ct, cg), dist(pe, cb)*2-dist(ct, cb)), col, tk, lt, *a1, an)
            img.ellipse(pe, (dist(ct, cd), dist(pe, cb)), col, tk, lt, *a2, an)
            img.ellipse(ct_sg(ctb, cb), (dist(ct, cg), dist(ctb, cb)/2), col, tk, lt, *a3, an)
        case "A6": ## 6
            a1 = (ang(180), ang(250))
            if "VM" in sty: a1 = [a%360 for a in a1]
            img.ellipse(pdb, (dist(cg, cd), dist(p1, pgb)), col, tk, lt, *a1, an)
            img.ellipse(ctb, (dist(cg, ct), dist(ct, ctb)), col, tk, lt, angle=an)
        case "A7": ## 7
            LINES += [[p1, phd], [phd, cb], [ctg, cd]]
        case "A8": ## 8
            img.ellipse(cth, (dist(ct, ct_sg(cd, ctd))*0.9, dist(cth, ch)), col, tk, lt, angle=an)
            img.ellipse(ctb, (dist(ct, ct_sg(cd, ctd)), dist(ctb, cb)), col, tk, lt, angle=an)
        case "A9": ## 9
            a1 = (ang(0), ang(70))
            if "VM" in sty and "HM" in sty: a1 = [a%360 for a in a1]
            img.ellipse(pgh, (dist(cg, cd), dist(p1, pgb)), col, tk, lt, *a1, an)
            img.ellipse(cth, (dist(cg, ct), dist(ct, ctb)), col, tk, lt, angle=an)
        case "B0": ## .
            img.circle(cb, fontSize*0.2, col, tk, lt)
        case "B1": ## ,
            LINES += [[p4, pts[2]]]
        case "B2": ## :
            img.circle(cb, fontSize*0.2, col, tk, lt)
            img.circle(ct, fontSize*0.2, col, tk, lt)
        case "B3": ## ;
            img.circle(ct, fontSize*0.2, col, tk, lt)
            LINES += [[p4, pts[2]]]
        case "B4": ## -
            LINES += [[ct_sg(cg, ctg), ct_sg(cd, ctd)]]
        case "B5": ## _
            LINES += [[p3, p4]]
        case "B6": ## !
            LINES += [[ch, ctb]]
            img.circle(cb, fontSize*0.2, col, tk, lt)
        case "B7": ## ?
            LINES += [[ct, ctb]]
            a1 = (ang(210), ang(450))
            if "HM" in sty: a1 = [a%360 for a in a1]
            img.ellipse(cth, (dist(ch, p1), dist(cth, ch)), col, tk, lt, *a1, an)
            img.circle(cb, fontSize*0.2, col, tk, lt)
        case "B8": ## ¡
            LINES += [[cth, cb]]
            img.circle(ch, fontSize*0.2, col, tk, lt)
        case "B9": ## ¿
            LINES += [[ct, cth]]
            a1 = (ang(30), ang(270))
            if "VM" in sty and not "HM" in sty: a1 = [a%360 for a in a1]
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a1, an)
            img.circle(ch, fontSize*0.2, col, tk, lt)
        case "C0": ## '
            LINES += [[ch, cth]]
        case "C1": ## "
            a = 3; LINES += [[pt_sg(ch, p1, a), pt_sg(cth, pgh, a)], [pt_sg(ch, p2, a), pt_sg(cth, pdh, a)]]
        case "C2": ## ·
            img.circle(ct, fontSize*0.2, col, tk, lt)
        case "C3": ## $
            LINES += [[ch, cb]]
            char.char = "A18"
            draw_char(img, char, ps, col, fs, tk, lt, an)
        case "C4": ## %
            LINES += [[ct2, ct3]]
            for pt in [ct1, ct4]:
                p = pt_sg(pt, ct, 5, 2)
                img.circle(p, dist(pt, p), col, tk, lt)
        case "C5": ## &
            p = pt_sg(cth, ch, 5, 2)
            r, r1, r2 = (dist(cth, ct1), dist(cth, ch)), (dist(ct1, p)*0.7, dist(p, ch)), (dist(ctb, pgb), dist(ctb, cb))
            a1, a2, a3 = (ang(140), ang(270)), (ang(270), ang(420)), [ang(-20), ang(220)]
            if "VM" in sty:
                if not "HM" in sty:
                    a1 = [a%360 for a in a1]
                    a3[1] -= 360
            if "HM" in sty:
                a2 = [a%360 for a in a2]
                if not "VM" in sty: a3[1] -= 360
                else: a3[0] -= 360
            img.ellipse(cth, r, col, tk, lt, *a1, an)
            img.ellipse(p, r1, col, tk, lt, *a2, an)
            img.ellipse(ctb, r2, col, tk, lt, *a3, an)
            LINES += [[coosEllipse(cth, r, a1[0], an), p4], [coosEllipse(p, r1, a2[1], an), coosEllipse(ctb, r2, a3[1], an)]]
        case "C6": ## /
            LINES += [[phd, pbg]]
        case "C7": ## =
            LINES += [[ct_sg(cg, ct1), ct_sg(cd, ct2)], [ct_sg(cg, ct3), ct_sg(cd, ct4)]]
        case "C8": ## +
            LINES += [[cth, ctb], [ct_sg(cg, ctg), ct_sg(cd, ctd)]]
        case "C9": ## *
            cs = ct, dist(ct, ct_sg(cd, ctd))
            LINES += [[coosCircle(*cs, a), coosCircle(*cs, a+180)] for a in [30, 90, 150]]
        case "D0": ## (
            if "HM" in sty: an += 180
            img.ellipse(ctd, (dist(ct, cg), dist(ct, ch)*1.2), col, tk, lt, 120, 240, an)
        case "D1": ## )
            if "HM" in sty: an += 180
            img.ellipse(ctg, (dist(ct, cg), dist(ct, ch)*1.2), col, tk, lt, 120, 240, an+180)
        case "D2": ## [
            LINES += [[phg, phd], [phg, pbg], [pbg, pbd]]
        case "D3": ## ]
            LINES += [[phg, phd], [phd, pbd], [pbg, pbd]]
        #################{}
        case "D6": ## |
            LINES += [[ch, cb]]
        case "D7": ## @
            a1, a2 = (ang(60), ang(360)), (ang(0), ang(90))
            if "VM" in sty:
                if "HM" in sty: a2 = [a%360 for a in a2]
                else: a1 = [a%360 for a in a1]
            img.ellipse(ct, (dist(ct, cd), dist(ct, cb)), col, tk, lt, *a1, an)
            img.ellipse(ct, (dist(ctb, ct4), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(ctd, (dist(ctd, cd), dist(ctd, ct4)), col, tk, lt, *a2, an)
            LINES += [[ct2, ct4]]
        case "D8": ## #
            LINES += [[ct_sg(cg, pgh), ct_sg(cd, pdh)], [ct_sg(cg, pgb), ct_sg(cd, pdb)], [ch, ct_sg(p3, pbg)], [ct_sg(p2, phd), cb]]
        case "D9": ## ¬
            LINES += [[cg, cd], [cd, pdb]]
        case "E0": ## º
            img.ellipse(cth, (dist(ct, cg), dist(ct, cth)), col, tk, lt, angle=an)
            LINES += [[pt_sg(cg, pgb, 2), pt_sg(cd, pdb, 2)]]
        case "E1": ## ª
            a1, a2 = [ang(90), ang(270)], [ang(180), ang(360)]
            if "VM" in sty and not "HM" in sty: a1[0] += 360; a2[0] += 360
            p = pt_sg(ct, ch, 3); d = (dist(ct, cd), dist(p, ct))
            pe = pt_sg(ch, cth, 2); de = (dist(ct, cd), dist(ch, pe))
            img.ellipse(p, d, col, tk, lt, *a1, an)
            img.ellipse(pe, de, col, tk, lt, *a2, an)
            LINES += [[pt_sg(cg, pgb, 2), pt_sg(cd, pdb, 2)], [coosEllipse(pe, de, ang(0), an), cd], [coosEllipse(p, d, ang(270), an), pdh], [ct, cd]]
        case "E2": ## `
            LINES += [[pt_sg(p1, p2, 2), pt_sg(pdh, pgh, 2)]]
        case "E3": ## ´
            LINES += [[pt_sg(p2, p1, 2), pt_sg(pgh, pdh, 2)]]
        case "E4": ## ^
            LINES += [[pt_sg(pdh, pgh, 4), ch], [ch, pt_sg(pgh, pdh, 4)]]
        case "E5": ## ¨
            img.circle(ct_sg(phg, ct1), fontSize*0.2*tk, col, -tk, lt)
            img.circle(ct_sg(phd, ct2), fontSize*0.2*tk, col, -tk, lt)
        case "E6": ## ~
            a1, a2 = (ang(180), ang(360)), (ang(0), ang(180))
            if "VM" in sty:
                if not "HM" in sty: a1 = (a%360 for a in a1)
                else: a1 = (a1[0], a1[1]-360)
            img.ellipse(ctg, (dist(ct, ctg), dist(ct, cth)/4), col, tk, lt, *a1, an)
            img.ellipse(ctd, (dist(ct, ctg), dist(ct, cth)/4), col, tk, lt, *a2, an)
        case "E7": ## €
            a1 = (ang(60), ang(300))
            if "VM" in sty and not "HM" in sty: a1 = (a%360 for a in a1)
            img.ellipse(ctd, (dist(ct, cg), dist(ch, ct)), col, tk, lt, *a1, an)
            LINES += [[ct_sg(pgh, cg), ct_sg(ct2, ctd)], [ct_sg(pgb, cg), ct_sg(ct4, ctd)]]
        case "E8": ## ¢
            p, r = ct, (dist(cb, p3), dist(ctb, cb))
            a1 = (ang(60), ang(300))
            if "VM" in sty and not "HM" in sty: a1 = (a%360 for a in a1)
            img.ellipse(p, r, col, tk, lt, *a1, an)
            pt = coosEllipse(p, r, ang(-90), an)
            LINES += [[ch, pt], [coosEllipse(p, r, ang(90), an), cb]]
        case "E9": ## ¶
            a1 = (ang(90), ang(270))
            if "VM" in sty and not "HM" in sty: a1 = (a%360 for a in a1)
            LINES += [[ch, cb], [ch, p2], [p2, p4]]
            img.ellipse(cth, (dist(ch, p1), dist(ch, cth)), col, 0, lt, *a1, an)
        case "F0": ## <
            LINES += [[ctd, ct3], [ct3, pbd]]
        case "F1": ## >
            LINES += [[ctg, ct4], [ct4, pbg]]
        case "F2": ## \
            LINES += [[phg, pbd]]
        case "F3": ## £
            p, r = cth, (dist(ct2, cth), dist(cth, ch)/2)
            img.ellipse(p, r, col, tk, lt, *(ang(180)%360, ang(360)) if "VM" in sty else (ang(180), ang(360)), angle=an)
            LINES += [[p3, p4], [cg, ctd], [coosEllipse(p, r, ang(180), an), ct3], [ct3, p3]]
        case "F4": ## ™
            LINES += [[p1, ch], [phg, ct1], [ch, cth], [p2, pdh], [ch, ct_sg(phd, ct2)], [ct_sg(phd, ct2), p2]]
        case "F5": ## ±
            LINES += [[ct3, ct4], [ctg, ctd], [ct_sg(cth, ct), ct_sg(ctb, ct)]]
        case "F6": ## ¦
            LINES += [[ch, ct_sg(cth, ct)], [cb, ct_sg(ctb, ct)]]
        case "F7": ## ©
            img.ellipse(cth, (dist(ct, cg), dist(cth, ch)), col, tk, lt, angle=an)
            img.ellipse(cth, (dist(ct, cg)/2, dist(cth, ch)/2), col, tk, lt, *(ang(50)%360, ang(310)) if "VM" in sty and not "HM" in sty else (ang(50), ang(310)), an)
        case "F8": ## ×
            LINES += [[pt_sg(ct1, ct, 2), pt_sg(ct4, ct, 2)], [pt_sg(ct2, ct, 2), pt_sg(ct3, ct, 2)]]
        case "F9": ## ÷
            LINES += [[ctg, ctd]]
            img.circle(ct_sg(cth, ct), fontSize*0.2, col, -tk, lt)
            img.circle(ct_sg(ctb, ct), fontSize*0.2, col, -tk, lt)
        case "G0": ## ’
            LINES += [[coosCircle(pdh, fs*0.2, an), coosCircle(cg, fs*0.2, 180+an)]]
        case "G1": ## «
            LINES += [[pgb, ct], [pgb, cb], [cd, ctb], [ctb, p4]]
        case "G2": ## »
            LINES += [[pdb, ct], [pdb, cb], [cg, ctb], [ctb, p3]]
        ## Letters #############################################
        case "A00": ## A
            LINES += [[p3, ch], [ch, p4], [ct_sg(p3, ch), ct_sg(ch, p4)]]
        case "A01": ## B
            LINES += [[p1, p3], [p3, cb], [cg, ct], [p1, ch]]
            a1 = (ang(270), ang(450))
            if "HM" in sty: an += 180
            img.ellipse(cth, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, *a1, an)
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, *a1, an)
        case "A02": ## C
            a1 = [ang(50), ang(300)]
            if "VM" in sty and not "HM" in sty: a1[0] += 360
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, *a1, an)
        case "A03": ## D
            LINES += [[p1, p3], [p3, cb], [p1, ch]]
            a1 = (ang(270), ang(450))
            if "VM" in sty and not "HM" in sty: a1 = [a1[0]%360, a1[1]]
            if "HM" in sty: an += 180
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, *a1, an)
        case "A04": ## E
            LINES += [[p1, p3], [cg, ctd], [p3, p4], [p1, pt_sg(p2, phd, 3)]]
        case "A05": ## F
            LINES += [[p1, p3], [cg, ctd], [p1, p2]]
        case "A06": ## G
            a1 = [ang(0), ang(300)]
            if "VM" in sty:
                if "HM" in sty: a1[1] += 360
                else: a1[0] += 360
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, *a1, an)
            LINES += [[ct, cd]]
        case "A07": ## H
            LINES += [[p1, p3], [p2, p4], [cg, cd]]
        case "A08": ## I
            LINES += [[p1, p2], [p3, p4], [ch, cb]]
        case "A09": ## J
            a = [ang(0), ang(135)]
            if "VM" in sty:
                if "HM" in sty: a[1] += 360
            LINES += [[phg, p2], [p2, pdb]]
            img.ellipse(ctb, (dist(pdb, ctb), dist(ctb, cb)), col, tk, lt, *a, an)
        case "A10": ## K
            p = pt_sg(cg, p3, 3)
            LINES += [[p1, p3], [p, p2], [pt_sg(p, p2, 2), p4]]
        case "A11": ## L
            LINES += [[p1, p3], [p3, p4]]
        case "A12": ## M
            LINES += [[p1, p3], [p1, pt_sg(ct, cb, 3)], [pt_sg(ct, cb, 3), p2], [p2, p4]]
        case "A13": ## N
            LINES += [[p1, p3], [p1, p4], [p2, p4]]
        case "A14": ## O
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, angle=an)
        case "A15": ## P
            LINES += [[p1, p3], [cg, ct], [p1, ch]]
            if "HM" in sty: an += 180
            img.ellipse(cth, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, *(ang(a) for a in (270, 450)), an)
        case "A16": ## Q
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, angle=an)
            LINES += [[ctb, p4]]
        case "A17": ## R
            LINES += [[p1, p3], [cg, ct], [p1, ch], [ct, p4]]
            if "HM" in sty: an += 180
            img.ellipse(cth, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, *(ang(a) for a in (270, 450)), an)
        case "A18": ## S
            pt1, pt2 = ct_sg(ch, ct), ct_sg(cb, ct)
            r = (dist(ct, cd), dist(pt1, ct))
            a1, a2 = [ang(90), ang(330)], [ang(-90), ang(160)]
            if "VM" in sty and not "HM" in sty: a1[0] += 360
            elif "VM" in sty: a2[1] += 360
            elif "HM" in sty: a2[0] += 360
            img.ellipse(pt1, (dist(ct, cd)*0.9, dist(pt1, ct)), col, tk, lt, *a1, an)
            img.ellipse(pt2, (dist(ct, cd), dist(pt1, ct)), col, tk, lt, *a2, an)
        case "A19": ## T
            LINES += [[p1, p2], [ch, cb]]
        case "A20": ## U
            LINES += [[p1, pgb], [p2, pdb]]
            if "VM" in sty: an+=180
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, 0, 180, an)
        case "A21": ## V
            LINES += [[p1, cb], [p2, cb]]
        case "A22": ## W
            LINES += [[p1, pbg], [ct, pbg], [ct, pbd], [p2, pbd]]
        case "A23": ## X
            LINES += [[p1, p4], [p2, p3]]
        case "A24": ## Y
            LINES += [[p1, ct], [p2, ct], [ct, cb]]
        case "A25": ## Z
            LINES += [[p1, p2], [p2, p3], [p3, p4]]
        case "A26": ## Æ
            LINES += [[p3, ch], [ch, cb], [ct_sg(p3, ch), cd], [ch, p2], [cb, p4]]
        case "A27": ## Œ
            a = [ang(90), ang(270)]
            if "VM" in sty and not "HM" in sty: a[0] += 360
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, *a, an)
            LINES += [[ch, cb], [ct, ct_sg(cd, ctd)], [cb, p4], [ch, p2]]
        case "A28": ## Þ
            LINES += [[p1, p3], [pgh, cth], [pgb, ctb]]
            if "HM" in sty: an+=180
            img.ellipse(ct, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, ang(270), ang(450), an)
        case "A29": ## Ð
            LINES += [[phg, pbg], [pbg, cb], [phg, ch], [cg, ct]]
            a1 = (ang(270), ang(450))
            if "VM" in sty and not "HM" in sty: a1 = [a1[0]%360, a1[1]]
            if "HM" in sty: an += 180
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, *a1, an)
        case "A30": ## А
            char.char = "A00"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A31": ## Б
            a = (ang(270), ang(450))
            if "HM" in sty: an+=180
            LINES += [[p1, p3], [p3, cb], [cg, ct], [p1, ct_sg(p2, phd)]]
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, *a, an)
        case "A32": ## В
            char.char = "A01"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A33": ## Г
            LINES += [[p1, p3], [p1, p2]]
        case "A34": ## Д
            LINES += [[pgb, p3], [pdb, p4], [pgb, pdb], [phg, ct_sg(phd, p2)], [ct_sg(phd, p2), ct_sg(ct4, pdb)]]
            a = [ang(0), ang(90)]
            if "HM" in sty and "VM" in sty: a[1]+=360
            img.ellipse(ct_sg(p1, phg), (dist(p1, phg)/2, dist(p1, pgb)), col, tk, lt, *a, an)
        case "A35": ## Е
            char.char = "A04"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A36": ## Ё
            for c in ["A35", "46"]:
                char.char = c
                draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A37": ## Ж
            LINES += [[p1, ctg], [ctg, p3], [ctg, ctd], [ch, cb], [p2, ctd], [ctd, p4]]
        case "A38": ## З
            a1, a2 = [ang(220), ang(450)], [ang(270), ang(500)]
            if "HM" in sty: a1, a2 = [a%360 for a in a1], [a%360 for a in a2]
            img.ellipse(cth, (dist(ch, p2)*0.9, dist(cth, ch)), col, tk, lt, *a1, an)
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, *a2, an)
        case "A39": ## И
            LINES += [[p1, p3], [p3, p2], [p2, p4]]
        case "A40": ## Й
            for c in ["A39", "48"]:
                char.char = c
                draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A41": ## К
            LINES += [[p1, p3], [cg, ctg], [ctg, p2], [ctg, p4]]
        case "A42": ## Л
            a = [ang(0), ang(90)]
            if "HM" in sty and "VM" in sty: a[1]+=360
            img.ellipse(p1, (dist(p1, phg), dist(p1, p3)), col, tk, lt, *a, an)
            LINES += [[phg, p2], [p2, p4]]
        case "A43": ## М
            LINES += [[p3, phg], [phg, ctb], [ctb, phd], [phd, p4]]
        case "A44": ## Н
            char.char = "A07"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A45": ## О
            char.char = "A14"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A46": ## П
            LINES += [[p1, p3], [p1, p2], [p2, p4]]
        case "A47": ## Р
            char.char = "A15"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A48": ## С
            char.char = "A02"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A49": ## Т
            char.char = "A19"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A50": ## У
            LINES += [[p2, p3], [p1, ct]]
        case "A51": ## Ф
            LINES += [[ch, cb], [phg, phd], [pbg, pbd]]
            img.ellipse(ct, (dist(ct, cd), dist(ct, pt_sg(cth, ch, 2))), col, tk, lt, angle=an)
        case "A52": ## Х
            char.char = "A23"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A53": ## Ц
            LINES += [[p1, p3], [p3, p4], [ct_sg(phd, p2), ct_sg(pbd, p4)], [p4, coosCircle(p4, fontSize, ang(90)+an)]]
        case "A54": ## Ч
            LINES += [[p2, p4], [p1, pgh], [ctd, cd]]
            img.ellipse(ct2, (dist(ct2, pgh), dist(cth, ct)), col, tk, lt, ang(90), ang(180), an)
        case "A55": ## Ш
            LINES += [[p1, p3], [p3, p4], [ch, cb], [p2, p4]]
        case "A56": ## Щ
            pt1, pt2 = ct_sg(phd, p2), ct_sg(pbd, p4)
            LINES += [[p1, p3], [p3, p4], [ct_sg(pt1, p1), ct_sg(pt2, p3)], [pt1, pt2], [p4, coosCircle(p4, fontSize, ang(90)+an)]]
        case "A57": ## Ъ
            LINES += [[p1, phg], [phg, pbg], [ctg, ct], [pbg, cb]]
            if "HM" in sty: an += 180
            img.ellipse(ctb, (dist(ch, p2), dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A58": ## Ы
            LINES += [[p1, p3], [cg, ctg], [p3, pbg], [p2, p4]]
            if "HM" in sty: an += 180
            img.ellipse(ct3, (dist(ch, p2), dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A59": ## Ь
            LINES += [[p1, p3], [cg, ct], [p3, cb]]
            if "HM" in sty: an += 180
            img.ellipse(ctb, (dist(ch, p2), dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A60": ## Э
            a = [ang(240), ang(490)]
            if "HM" in sty:
                if "VM" in sty: a[1] += 360
                else: a[0] += 360
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, *a, an)
            LINES += [[ct, cd]]
        case "A61": ## Ю
            img.ellipse(ct_sg(ct, ctd), (dist(ct_sg(ct, ctd), cd), dist(ct, ch)), col, tk, lt, angle=an)
            LINES += [[p1, p3], [cg, ctg]]
        case "A62": ## Я
            char.char = "A17"
            if "HM" in sty: char.style = ":".join(i for i in sty.split(":") if not i == "HM")
            else: char.style += ":HM"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A63": ## Đ
            char.char = "A29"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        ##################
        case "A70": ## Α
            char.char = "A00"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A71": ## Β
            char.char = "A01"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A72": ## Γ
            char.char = "A33"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A73": ## Δ
            LINES += [[p3, ch], [ch, p4], [p3, p4]]
        case "A74": ## Ε
            char.char = "A04"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A75": ## Ζ
            char.char = "A25"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A76": ## Η
            char.char = "A07"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A77": ## Θ
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, angle=an)
            LINES += [[cg, cd]]
        case "A78": ## Ι
            char.char = "A08"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A79": ## Κ
            char.char = "A41"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A80": ## Λ
            LINES += [[p3, ch], [ch, p4]]
        case "A81": ## Μ
            char.char = "A12"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A82": ## Ν
            char.char = "A13"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A83": ## Ξ
            LINES += [[p1, p2], [p3, p4], [ctg, ctd]]
        case "A84": ## Ο
            char.char = "A14"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A85": ## Π
            char.char = "A46"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A86": ## Ρ
            char.char = "A15"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A87": ## Σ
            LINES += [[p1, p2], [p3, p4], [p1, ct], [ct, p3]]
        case "A88": ## Σ
            LINES += [[p1, p2], [p1, p4], [p4, p3]]
        case "A89": ## Τ
            char.char = "A19"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A90": ## Υ
            LINES += [[p1, ct], [p2, ct], [ct, cb]]
        case "A91": ## Φ
            char.char = "A51"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A92": ## Χ
            char.char = "A23"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "A93": ## Ψ
            c, d = cth, (dist(ct, cd), dist(ct, ch))
            a = [ang(0), ang(180)]
            if "HM" in sty and "VM" in sty: a[1] += 360
            img.ellipse(c, d, col, tk, lt, *a, an)
            LINES += [[ch, cb], [coosEllipse(c, d, a[0], an), p2], [coosEllipse(c, d, a[1], an), p1]]
        case "A94": ## Ω
            y, a, b = dist(ct, ch), ang(140), ang(400)
            if "VM" in sty:
                if "HM" in sty: b += 360
                else: a += 360
            elif "HM" in sty: a += 360
            p, d = [ct[0], ct[1]-dist(ct, ch)+y], (dist(ct, cd), y)
            img.ellipse(p, d, col, tk, lt, a, b, an)
            LINES += [[p3, pbg], [coosEllipse(p, d, a, an), pbg], [coosEllipse(p, d, b, an), pbd], [pbd, p4]]
        ########################################################
        case "B00": # a
            a1, a2 = [ang(90), ang(270)], [ang(180), ang(360)]
            if "VM" in sty and not "HM" in sty: a1[0] += 360; a2[0] += 360
            p = pt_sg(cb, ct, 3); d = (dist(ct, cd), dist(p, cb))
            pe = pt_sg(ct, ctb, 2); de = (dist(ct, cd), dist(ct, pe))
            img.ellipse(p, d, col, tk, lt, *a1, an)
            img.ellipse(pe, de, col, tk, lt, *a2, an)
            LINES += [[coosEllipse(pe, de, ang(0), an), p4], [coosEllipse(p, d, ang(270), an), pdb], [cb, p4]]
        case "B01": # b
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[pgh, p3]]
        case "B02": # c
            a = [ang(60), ang(300)]
            if "VM" in sty and not "HM" in sty: a[0] += 360
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a, an)
        case "B03": # d
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[pdh, p4]]
        case "B04": # e
            a = [ang(30), ang(360)]
            if "VM" in sty and not "HM" in sty: a[0] += 360
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a, an)
            LINES += [[pgb, pdb]]
        case "B05": # f
            a = [ang(180), ang(300)]
            if "VM" in sty and not "HM" in sty: a[0] += 360
            img.ellipse(cd, (dist(ct, cd), dist(ct, cth)), col, tk, lt, *a, an)
            LINES += [[cg, cd], [ct, cb]]
        case "B06": # g
            a = [ang(0), ang(150)]
            if "VM" in sty and "HM" in sty: a[1] += 360
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(cb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a, an)
            LINES += [[cd, p4]]
        case "B07": # h
            a = [ang(180), ang(360)]
            if "VM" in sty and not "HM" in sty: a[0] += 360
            img.ellipse(ctb, (dist(ct, cg), dist(ct, ctb)), col, tk, lt, *a, an)
            LINES += [[pgh, p3], [pdb, p4]]
        case "B08": # i
            LINES += [[p3, p4], [ct, cb], [cg, ct]]
            if not char.diacr: img.circle(cth, fontSize*0.2, col, tk, lt)
        case "B09": # j
            a = [ang(0), ang(90)]
            if "VM" in sty and "HM" in sty: a[1] += 360
            LINES += [[ct, cb], [cg, ct]]
            if not char.diacr: img.circle(cth, fontSize*0.2, col, tk, lt)
            img.ellipse(p3, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a, an)
        case "B10": # k
            LINES += [[pgh, p3], [pt_sg(pgb, cd, 2), p4], [pgb, cd]]
        case "B11": # l
            a = [ang(90), ang(180)]
            LINES += [[pgh, cth], [cth, ctb]]
            img.ellipse(pdb, (dist(ctb, pgb), dist(ctb, cb)), col, tk, lt, *a, an)
        case "B12": # m
            a = [ang(180), ang(360)]
            if "VM" in sty and not "HM" in sty: a[0] += 360
            LINES += [[cg, p3], [ctb, cb], [pdb, p4]]
            img.ellipse(ct3, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, *a, an)
            img.ellipse(ct4, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, *a, an)
        case "B13": # n
            a = [ang(180), ang(360)]
            if "VM" in sty and not "HM" in sty: a[0] += 360
            LINES += [[cg, p3], [pdb, p4]]
            img.ellipse(ctb, (dist(ct, cd), dist(ct, ctb)), col, tk, lt, *a, an)
        case "B14": # o
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
        case "B15": # p
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[cg, coosCircle(p3, dist(ct, ctb), ang(90)+an)]]
        case "B16": # q
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[cd, coosCircle(p4, dist(ct, ctb), ang(90)+an)]]
        case "B17": # r
            r, a = (dist(pgb, pdb), dist(pdb, cd)), 270
            a1 = [ang(180), ang(a)]
            if "VM" in sty and not "HM" in sty: a1[0] += 360
            img.ellipse(pdb, r, col, tk, lt, *a1, an)
            LINES += [
                [cg, p3], [coosCircle(p3, fontSize/2, ang(180)+an), pbg],
                [coosCircle(cg, fontSize/2, ang(180)+an), cg], [cd, coosCircle(cd, fontSize/2, ang(90)+an)]
            ]
        case "B18": # s
            a1, a2 = [ang(90), ang(330)], [ang(-90), ang(160)]
            if "VM" in sty and not "HM" in sty: a1[0] += 360
            elif "VM" in sty: a2[1] += 360
            elif "HM" in sty: a2[0] += 360
            pt1, pt2 = ct_sg(ct, ctb), ct_sg(cb, ctb)
            r = (dist(ct, cd), dist(pt1, ct))
            img.ellipse(pt1, (dist(ct, cd)*0.9, dist(pt1, ct)), col, tk, lt, *a1, an)
            img.ellipse(pt2, (dist(ct, cd), dist(pt1, ct)), col, tk, lt, *a2, an)
        case "B19": # t
            LINES += [[cth, ctb], [cg, cd]]
            img.ellipse(pdb, (dist(ctb, pgb), dist(ctb, cb)), col, tk, lt, ang(90), ang(180), an)
        case "B20": # u
            a = [ang(0), ang(180)]
            if "VM" in sty and "HM" in sty: a[1] += 360
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a, an)
            LINES += [[cg, pgb], [cd, p4]]
        case "B21": # v
            LINES += [[cg, cb], [cd, cb]]
        case "B22": # w
            LINES += [[cg, pbg], [pbg, ct_sg(ctb, ct)], [ct_sg(ctb, ct), pbd], [pbd, cd]]
        case "B23": # x
            LINES += [[cg, p4], [cd, p3]]
        case "B24": # y
            a = [ang(0), ang(90)]
            if "VM" in sty and "HM" in sty: a[1] += 360
            img.ellipse(p3, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a, an)
            LINES += [[cg, cb], [cd, cb]]
        case "B25": # z
            LINES += [[cg, cd], [cd, p3], [p3, p4]]
        case "B26": # æ
            p = pt_sg(pbg, ctg, 3); d = (dist(cg, ctg), dist(p, pbg))
            pe = pt_sg(ctg, ct3); de = (dist(cg, ctg), dist(pe, ctg))
            a1, a2, a3, a4 = [ang(90), ang(270)], [ang(180), ang(360)], [ang(180), ang(450)], [ang(0), ang(90)]
            if "VM" in sty:
                if "HM" in sty:
                    a4[1] += 360
                    a3[1] += 360
                else:
                    a1[0] += 360
                    a2[0] += 360
                    a3[0] += 360
            elif "HM" in sty:
                a3[0] += 360
            img.ellipse(p, d, col, tk, lt, *a1, an)
            img.ellipse(pe, de, col, tk, lt, *a2, an)
            img.ellipse(pt_sg(ctd, ct4), de, col, tk, lt, *a3, an)
            img.ellipse(pt_sg(p4, ctb), de, col, tk, lt, *a4, an)
            LINES += [[coosEllipse(pe, de, ang(0), an), cb], [pbg, pbd], [ct3, ct4]]
        case "B27": # œ
            a = [ang(50), ang(360)]
            if "VM" in sty and not "HM" in sty: a[0]+=360
            img.ellipse(ct3, (dist(ct, ctg)*1.1, dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(ct4, (dist(ct, ctg)*1.1, dist(ctb, cb)), col, tk, lt, *a, an)
            LINES += [[ctb, pdb]]
        case "B28": # þ
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[pgh, coosCircle(p3, dist(ct, ctb), ang(90)+an)]]
        case "B29": # ð
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(pgb, (dist(cg, cd), dist(ct, cb)), col, tk, lt, ang(270), ang(360), an)
            LINES += [[pt_sg(cg, pgh, 2), pdh]]
        case "B30": # а
            LINES += [[p3, ct], [ct, p4], [pt_sg(p3, ct, 2), pt_sg(p4, ct, 2)]]
        case "B31": # б
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            p, p1 = ctb, ct_sg(ch, phd)
            r, r1 = (dist(ct, cg), dist(ctb, cth)), (dist(ct, cg), dist(ch, cth))
            an1, an2 = ang(270), ang(90)
            a1, a2 = ang(180), ang(60)
            if "VM" in sty and not "HM" in sty: a1+=360
            img.ellipse(p, r, col, tk, lt, a1, an1, an)
            img.ellipse(p1, r1, col, tk, lt, a2, an2, an)
            LINES += [[coosEllipse(p, r, an1, an), coosEllipse(p1, r1, an2, an)]]
        case "B32": # в
            LINES += [[cg, p3], [pgb, ctb], [cg, ct], [p3, cb]]
            if "HM" in sty: an+=180
            img.ellipse(ct_sg(ctb, ct), (dist(ct, cd)*0.8, dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
            img.ellipse(ct_sg(ctb, cb), (dist(ct, cd), dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B33": # г
            LINES += [[cg, p3], [cg, cd]]
        case "B34": # д
            LINES += [[ct_sg(pgb, p3), p3], [ct_sg(pdb, p4), p4], [ct_sg(pgb, p3), ct_sg(pdb, p4)], [pt_sg(ct, cg, 2), ct_sg(ct, cd)], [ct_sg(ct, cd), ct_sg(ctb, p4)]]
            a = ang(90)
            if "HM" in sty and "VM" in sty: a += 360
            img.ellipse(pt_sg(cg, ct, 2), (dist(pt_sg(cg, ct, 2), pt_sg(ct, cg, 2)), dist(ct, ct_sg(ctb, cb))), col, tk, lt, ang(0), a, an)
        case "B35": # е
            LINES += [[cg, cd], [cg, p3], [pgb, ct_sg(ctb, pdb)], [p3, p4]]
        case "B36": # ё
            for c in ["B35", "46"]:
                char.char = c
                draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "B37": # ж
            pt1, pt2 = ct_sg(pgb, ctb), ct_sg(pdb, ctb)
            LINES += [[cg, pt1], [pt1, pt2], [pt1, p3], [ct, cb], [cd, pt2], [pt2, p4]]
        case "B38": # з
            a1, a2 = [ang(220), ang(450)], [ang(270), ang(500)]
            if "HM" in sty: a1, a2 = [a%360 for a in a1], [a%360 for a in a2]
            img.ellipse(ct_sg(ct, ctb), (dist(ct, cd)*0.9, dist(ct, ctb)/2), col, tk, lt, *a1, an)
            img.ellipse(ct_sg(cb, ctb), (dist(ct, cd), dist(ctb, cb)/2), col, tk, lt, *a2, an)
        case "B39": # и
            LINES += [[cg, p3], [cd, p4], [cd, p3]]
        case "B40": # й
            for c in ["B39", "48"]:
                char.char = c
                draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "B41": # к
            LINES += [[cg, p3], [pgb, ctb], [ctb, cd], [ctb, p4]]
        case "B42": # л
            a = ang(90)
            if "HM" in sty and "VM" in sty: a += 360
            img.ellipse(cg, (dist(cg, ct_sg(cg, ct)), dist(ct, cb)), col, tk, lt, ang(0), a, an)
            LINES += [[ct_sg(cg, ct), cd], [cd, p4]]
        case "B43": # м
            LINES += [[p3, ct_sg(cg, ctg)], [ct_sg(cg, ctg), ct_sg(ctb, cb)], [ct_sg(ctb, cb), ct_sg(cd, ctd)], [ct_sg(cd, ctd), p4]]
        case "B44": # н
            LINES += [[cg, p3], [pgb, pdb], [cd, p4]]
        case "B45": # о
            char.char = "B14"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "B46": # п
            LINES += [[cg, p3], [cg, cd], [cd, p4]]
        case "B47": # р
            LINES += [[cg, p3], [pgb, ctb], [cg, ct]]
            if "HM" in sty: an+=180
            img.ellipse(ct_sg(ctb, ct), (dist(ct, cd)*0.8, dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B48": # с
            char.char = "B02"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "B49": # т
            LINES += [[ct, cb], [cg, cd]]
        case "B50": # у
            char.char = "B24"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "B51": # ф
            LINES += [[cth, coosCircle(cb, dist(ct, cth), ang(90)+an)]]
            a1, a2 = [ang(65), ang(295)], [ang(245), ang(475)]
            if "VM" in sty and not "HM" in sty: a1[0] += 360
            if "HM" in sty:
                if "VM" in sty: a2[1]+=360
                else: a2[0] += 360
            img.ellipse(ct_sg(pgb, ctb), (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a1, an)
            img.ellipse(ct_sg(pdb, ctb), (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a2, an)
        case "B52": # х
            LINES += [[cg, p4], [cd, p3]]
        case "B53": # ц
            LINES += [[cg, p3], [p3, p4], [ct_sg(cd, ct), ct_sg(p4, cb)], [p4, coosCircle(p4, fontSize*0.5, ang(90)+an)]]
        case "B54": # ч
            LINES += [[cd, p4], [cg, ct_sg(cg, pgb)], [ct_sg(ctb, pdb), pdb]]
            pt = ct_sg(cd, ctb)
            img.ellipse(pt, (dist(pt, ct_sg(cg, pgb)), dist(cd, pdb)/2), col, tk, lt, ang(90), ang(180), an)
        case "B55": # ш
            LINES += [[cg, p3], [p3, p4], [ct, cb], [cd, p4]]
        case "B56": # щ
            pt1, pt2 = ct_sg(cd, ct), ct_sg(p4, cb)
            LINES += [[cg, p3], [ct_sg(cg, pt1), ct_sg(p3, pt2)], [p3, p4], [pt1, pt2], [p4, coosCircle(p4, fontSize*0.5, ang(90)+an)]]
        case "B57": # ъ
            if "HM" in sty: an+=180
            LINES += [[cg, ct_sg(cg, ct)], [ct_sg(cg, ct), ct_sg(p3, cb)], [ct_sg(p3, cb), cb], [ct_sg(pgb, ctb), ctb]]
            img.ellipse(ct_sg(ctb, cb), (dist(ct, cd), dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B58": # ы
            if "HM" in sty: an+=180
            LINES += [[cg, p3], [pgb, ctb], [cd, p4], [p3, cb]]
            img.ellipse(ct_sg(ctb, cb), (dist(ct, ctd)*0.7, dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B59": # ь
            if "HM" in sty: an+=180
            LINES += [[cg, p3], [pgb, ctb], [p3, cb]]
            img.ellipse(ct_sg(ctb, cb), (dist(ct, cd), dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B60": # э
            a = ang(240)
            if "HM" in sty:
                if "VM" in sty: a -= 360
                else: a += 360
            img.ellipse(ctb, (dist(ct, cd), dist(ct, ctb)), col, tk, lt, a, ang(490), an)
            LINES += [[ctb, pdb]]
        case "B61": # ю
            p = ct_sg(ctb, pdb)
            r = (dist(p, pdb), dist(ct, ctb))
            img.ellipse(p, r, col, tk, lt, angle=an)
            LINES += [[cg, p3], [pgb, coosEllipse(p, r, ang(180), an)]]
        case "B62": # я
            LINES += [[cd, p4], [pdb, ctb], [cd, ct], [ctb, p3]]
            if "HM" in sty: an+=180
            img.ellipse(ct_sg(ctb, ct), (dist(ct, cd)*0.8, dist(ct, ctb)/2), col, tk, lt, 90, 270, an)
        case "B63": # đ
            char.char = "B03"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
            p = ct_sg(ct2, ct)
            LINES += [[p, coosCircle(p, dist(p, ct_sg(pdh, cd))*2, ang(0)+an)]]
        #################
        case "B70": # α
            if "HM" in sty: an+=180
            img.ellipse(coosCircle(pgb, dist(ct, cg)*0.82, ang(0)), (dist(ctb, pgb), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(coosCircle(pdb, dist(ct, cg)*0.82, ang(0)), (dist(ctb, pdb), dist(ctb, cb)), col, tk, lt, 120, 240, angle=an)
        case "B71": # β
            a1, a2, a3, a4, a5 = [ang(180), ang(270)], [ang(270), ang(360)], [ang(0), ang(90)], [ang(270), ang(360)], [ang(0), ang(120)]
            if "VM" in sty:
                a1[0] += 360
                if "HM" in sty:
                    a1[1] += 360
                    a3[1] += 360
                    a5[1] += 360
            LINES += [[coosCircle(p3, dist(cb, ct_sg(*pts[2::])), ang(90)+an), cg]]
            img.ellipse(ct, (dist(ct, cg), dist(cth, ct)), col, tk, lt, *a1, an)
            img.ellipse(ct, (dist(ct, cg)*0.7, dist(cth, ct)), col, tk, lt, *a2, an)
            img.ellipse(ct, (dist(ct, cg)*0.7, dist(cth, ct)*0.6), col, tk, lt, *a3, an)
            img.ellipse(ctb, (dist(ct, cg), dist(ctb, ct)*0.6), col, tk, lt, *a4, an)
            img.ellipse(ctb, (dist(ct, cg), dist(ctb, ct)), col, tk, lt, *a5, an)
        case "B72": # γ
            rs = (dist(cb, p3), dist(cb, ct))
            img.ellipse(p3, rs, col, tk, lt, ang(-70), ang(-10), an)
            img.ellipse(p4, rs, col, tk, lt, ang(190), ang(250), an)
            img.ellipse(cb, (dist(cb, p3)*0.1, dist(cb, coosEllipse(p3, rs, ang(-10), an))), col, tk, lt, ang(0)+360, ang(360)%360, an)
        case "B73": # δ
            p, rs = ctb, (dist(cb, p3), dist(ctb, cb))
            img.ellipse(p, rs, col, tk, lt, angle=an)
            LINES += [[ct_sg(ct2, phd), ct1], [ct1, coosEllipse(p, rs, ang(-60), an)]]
        case "B74": # ε
            rs = (dist(cb, p3), dist(cb, ctb)/2)
            a = 360 if "VM" in sty and not "HM" in sty else 0
            img.ellipse(ct_sg(ct, ctb), rs, col, tk, lt, ang(90)+a, ang(310), an)
            img.ellipse(ct_sg(cb, ctb), rs, col, tk, lt, ang(40)+a, ang(270), an)
            LINES += [[ctb, ct_sg(ctb, pdb)]]
        case "B75": # ζ
            V, H = "VM" in sty, "HM" in sty
            A, B, d = ang(75), ang(210), dist(p4, pts[-1])/2
            p, rs, a = ctb, (dist(ct, cg), dist(ctb, ct)), an+(-20 if (H or V) and (H!=V) else 20)
            p2, rs2 = p4, (d*0.7, d*0.5)
            a1, a2 = [A, B], [ang(-90), ang(120)]
            if V and not H: a1[0]+=360
            if H: a2[0]+=360
            img.ellipse(p, rs, col, tk, lt, *a1, a)
            img.ellipse(p2, rs2, col, tk, lt, *a2, an)
            LINES += [[pgh,  pdh], [pdh, coosEllipse(p, rs, B, a)], [coosEllipse(p, rs, A, a), coosEllipse(p2, rs2, ang(270), an)]]
        case "B76": # η
            a = 180 if "VM" in sty else 0
            LINES += [[cg, p3], [pdb, coosCircle(p4, dist(p4, pts[-1]), ang(90)+an)]]
            img.ellipse(ctb, (dist(ct, cd), dist(ct, ctb)), col, tk, lt, 180+a, 360+a, an)
        case "B77": # θ
            p = ct_sg(ct, ctb)
            rs = (dist(ct, cg), dist(p, cb))
            img.ellipse(p, rs, col, tk, lt, angle=an)
            LINES += [[coosEllipse(p, rs, i, an) for i in (0, 180)]]
        case "B78": # ι
            LINES += [[ct, ctb]]
            img.ellipse(pdb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, ang(90), ang(180), an)
        case "B79": # κ
            p = pt_sg(pgb, ctb, 2)
            LINES += [[cg, p3], [pgb, p], [p, cd], [p, p4]]
        case "B80": # λ
            l = [phg, p4]
            LINES += [l, [ct_sg(*l), p3]]
        case "B81": # μ
            a = 180 if "VM" in sty else 0
            img.ellipse(ctb, (dist(ct, cd), dist(ct, ctb)), col, tk, lt, a, a+180, an)
            LINES += [[cg, coosCircle(p3, dist(p4, pts[-1]), ang(90)+an)], [cd, p4]]
        case "B82": # ν
            a = 360 if "HM" in sty and not "VM" in sty else 0
            img.ellipse(p3, (dist(cb, p3), dist(cb, ct)), col, tk, lt, ang(-70)+a, ang(0), an)
            LINES += [[cb, cd]]
        case "B83": # ξ
            V, H = "VM" in sty, "HM" in sty
            p, pt = pt_sg(cth, cb, 3), pt_sg(cb, cth, 3)
            A, B, d = ang(75), ang(210), dist(p4, pts[-1])/2
            a1, a2, ag = [A, B], [ang(-90), ang(120)], ang(90)
            if V and not H: a1[0]+=360; ag+=360
            img.ellipse(p, (dist(p1, ch), dist(cth, p)), col, tk, lt, ag, ang(270), an)
            p, rs, a = ctb, (dist(ct, cg), dist(ctb, ct)), an+(-20 if (H or V) and (H!=V) else 20)
            p2, rs2 = p4, (d*0.7, d*0.5)
            if H: a2[0]+=360
            img.ellipse(p, rs, col, tk, lt, *a1, a)
            img.ellipse(p2, rs2, col, tk, lt, *a2, an)
            LINES += [[pgh, pdh], [ct_sg(ct, ctb), ct_sg(cd, pdb)], [coosEllipse(p, rs, A, a), coosEllipse(p2, rs2, ang(270), an)]]
        case "B84": # ο
            char.char = "B14"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "B85": # π
            char.char = "B46"
            draw_char(img, char, points, col, fs, tk, lt, an, False)
        case "B86": # ρ
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(ctb, (dist(ct, cd), dist(ct, cb)), col, tk, lt, ang(60), ang(180), an)
        case "B87": # σ
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[ct, coosCircle(cd, fs*0.3, ang(an))]]
        case "B88": # ς
            a1, a2, d = [ang(90), ang(340)], [ang(-90), ang(120)], dist(p4, pts[-1])
            if "HM" in sty:
                if "VM" in sty: a2[1] += 360
                else: a2[0] += 360
            elif "VM" in sty and not "HM" in sty: a1[0] += 360
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, *a1, an)
            img.ellipse(ct_sg(*pts[2::]), (d*0.7, d*0.5), col, tk, lt, *a2, an)
        case "B89": # τ
            LINES += [[ct, ctb], [cg, cd]]
            img.ellipse(pdb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, ang(90), ang(180), an)
        case "B90": # υ
            p, r = ctb, (dist(cg, ct), dist(ctb, cb))
            img.ellipse(p, r, col, tk, lt, ang(0), ang(150)+(360 if "HM" in sty and "VM" in sty else 0), an)
            LINES += [[cg, coosEllipse(p, r, ang(150), an)], [cd, pdb]]
        case "B91": # φ
            a1, a2, a3, a4 = [ang(0), ang(180)], [ang(180), ang(270)], [ang(270), ang(360)], [ang(180), ang(270)]
            if "VM" in sty:
                if "HM" in sty: a1[1]+=360
                else: a4[0]+=360;a2[0]+=360
            img.ellipse(ctb, (dist(cg, ct), dist(ct, ctb)), col, tk, lt, *a1, an)
            img.ellipse(ct_sg(ct, ct4), (dist(ctg, ct)/2, dist(cth, ct)/2), col, tk, lt, *a2, an)
            img.ellipse(ct4, (dist(cg, ctg), dist(cth, ct)), col, tk, lt, *a3, an)
            img.ellipse(ct3, (dist(cg, ctg), dist(cth, ct)), col, tk, lt, *a4, an)
            LINES += [[ct_sg(ct, ctb), coosCircle(ct_sg(*pts[2::]), dist(p4, pts[-1]), ang(90)+an)]]
        case "B92": # χ
            da = dist(p4, pts[-1])*1.75, ang(90)+an
            LINES += [[cg, coosCircle(p4, *da)], [cd, coosCircle(p3, *da)]]
        case "B93": # ψ
            a1 = [ang(0), ang(180)]
            if "VM" in sty and "HM" in sty: a1[1]+=360
            img.ellipse(ctb, (dist(cg, ct), dist(ct, ctb)), col, tk, lt, *a1, an)
            LINES += [[pgb, cg], [pdb, cd], [ct, coosCircle(ct_sg(*pts[2::]), dist(p4, pts[-1]), ang(90)+an)]]
        case "B94": # ω
            r = (dist(ctg, ct), dist(ctb, ct))
            a1, a2 = [ang(0), ang(270)], [ang(-90), ang(180)]
            if "VM" in sty: a1[1 if "HM" in sty else 0] += 360
            if "HM" in sty: a2[1 if "VM" in sty else 0] += 360
            img.ellipse(ct3, r, col, tk, lt, *a1, an)
            img.ellipse(ct4, r, col, tk, lt, *a2, an)
        ### Emojis ######################################
        case "A000": ...
    #################################################
        case _: ## Other chars
            if "<" in str(char): ## Unknown character ##
                char.char = "00"
                draw_char(img, char, points, col, fs, tk, lt, an, False)
            else: ## Unassigned pattern character ##
                LINES += [[p1, p4], [p2, p3], [p1, p2], [p1, p3], [p2, p4], [p3, p4]]
    for a, b in LINES: img.line(a, b, col, tk, lt)
    #################################################
    if help:
        d = 3
        img.circle(pts[0], d*2, COL.compl(COL.help), 0)
        for p in pts[:-1:]: img.circle(p, d, COL.help, 0)
        t = str(char).replace(":", "\n")
        while "(" in t: t = t[:t.index("("):]+t[1+t.index(")")::]
        img.text(t.strip("<").strip(">"), pts[0], COL.help, fontSize=3, thickness=2, centered=False)
    return ##########################################