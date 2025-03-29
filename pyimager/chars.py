try: from pyimager.main import *
except: from main import *

def get_coos(ps):
    ct = ct_cr(*ps)
    p1, p2, p3, p4 = ps
    ch, cb, cg, cd = ct_sg(p1, p2), ct_sg(p3, p4), ct_sg(p1, p3), ct_sg(p2, p4)
    cth, ctb, ctg, ctd = ct_sg(ct, ch), ct_sg(ct, cb), ct_sg(ct, cg), ct_sg(ct, cd)
    ct1, ct2, ct3, ct4 = ct_sg(ct, p1), ct_sg(ct, p2), ct_sg(ct, p3), ct_sg(ct, p4)
    phg, phd, pbg, pbd = ct_sg(p1, ch), ct_sg(p2, ch), ct_sg(p3, cb), ct_sg(p4, cb)
    pgh, pdh, pgb, pdb = ct_sg(p1, cg), ct_sg(p2, cd), ct_sg(p3, cg), ct_sg(p4, cd)
    return ct,p1,p2,p3,p4,ch,cb,cg,cd,cth,ctb,ctg,ctd,ct1,ct2,ct3,ct4,phg,phd,pbg,pbd,pgh,pdh,pgb,pdb

def draw_char(img, char, pts, colour=COL.red, fontSize=1, thickness=1, lineType=0, angle=0, help=False, format={}):
    ## VARS ##
    col, fs, tk, lt, an = colour, fontSize, thickness, lineType, angle
    ct = ct_cr(*pts)
    ps = [coosCircle(p, fontSize, a+an) for p, a in zip(pts, (45, 135, 315, 225))]
    vert = horz = False
    ## Modif vars selon style ## Latin chars would be the only ones supported officially ##
    LINES = []
    if not (type(char)==str or not ":" in str(char)): ### Adapter les variables selon le style à appliquer
        lc = col
        c, s = str(char).split(":")[0], str(char).split(":")[1::]
        if "OL" in s: LINES += [[ct_sg(pts[0], pts[2]), ct_sg(pts[1], pts[3])]]
        if "UL" in s: LINES += [[pts[2], pts[3]]]
        if "TL" in s: LINES += [[pts[0], pts[1]]]
        if "TN" in s: tk = 1 if tk <= 1 else tk/2
        if "BD" in s: tk *= 2
        if "IT" in s:
            ps[:2:] = (coosCircle(p, fontSize, an) for p in (ps[0], ps[1]))
            an += (angleInterPoints(ps[1], ps[-1])-90)/2
        if "CI" in s:
            ps[:2:] = (coosCircle(p, fontSize, an+180) for p in (ps[0], ps[1]))
            an += (angleInterPoints(ps[1], ps[-1])-90)/2
        if "VM" in s:
            o = (2, 3, 0, 1)
            ps, pts = [ps[i] for i in o], [pts[i] for i in o]
            vert = True ## Repair chars that would appear incorrectly
        if "HM" in s:
            o = (1, 0, 3, 2)
            ps, pts = [ps[i] for i in o], [pts[i] for i in o]
            horz = True ## Repair chars that would appear incorrectly
        for st in (i for i in s if len(i) == 10):
            if   "BG" in st: img.polygon([pts[i] for i in (0, 1, 3, 2)], COL.new(st[3:-1:]), 0)
            elif "FG" in st: col = COL.new(st[3:-1:])
            elif "LS" in st: lc = COL.new(st[3:-1:])
        for a, b in LINES: img.line(a, b, lc, tk*1.5, lt)
        LINES = []
    ct,p1,p2,p3,p4,ch,cb,cg,cd,cth,ctb,ctg,ctd,ct1,ct2,ct3,ct4,phg,phd,pbg,pbd,pgh,pdh,pgb,pdb = get_coos(ps)
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
        ### Diacritiques suscrits ##############################
        case "40": # `
            if char.upper: LINES += [[pt_sg(*pts[:2:], 2), pt_sg(p2, p1, 2)]]
            else: LINES += [[pt_sg(ct1, ct2, 2), pt_sg(ct_sg(cd, pdh), ct_sg(cg, pgh), 2)]]
        case "41": # ´
            if char.upper: LINES += [[pt_sg(*pts[1::-1], 2), pt_sg(p1, p2, 2)]]
            else: LINES += [[pt_sg(ct2, ct1, 2), pt_sg(ct_sg(cg, pgh), ct_sg(cd, pdh), 2)]]
        case "42": # ^
            if char.upper: LINES += [[pt_sg(p2, p1, 2), ct_sg(*pts[1::-1])], [ct_sg(*pts[1::-1]), pt_sg(p1, p2, 2)]]
            else: LINES += [[ct_sg(cg, cth), cth], [cth, ct_sg(cd, cth)]]
        case "43": # ˇ
            if char.upper: LINES += [[pt_sg(*pts[1::-1], 2), ch], [ch, pt_sg(*pts[:2:], 2)]]
            else: LINES += [[ct1, ct_sg(cth, ct)], [ct_sg(cth, ct), ct2]]
        case "44": # ̏
            if char.upper: LINES += [[ch, pt_sg(*pts[:2:], 3, 2)], [ct_sg(phd, ch), pt_sg(*pts[:2:], 3, 3)]]
            else: LINES += [[ct1, ct_sg(cth, ct)], [cth, ct_sg(ctd, ct2)]]
        case "45": # ̋
            if char.upper: LINES += [[ch, pt_sg(*pts[1::-1], 3, 2)], [ct_sg(phg, ch), pt_sg(*pts[1::-1], 3, 3)]]
            else: LINES += [[ct2, ct_sg(cth, ct)], [cth, ct_sg(ctg, ct1)]]
        case "46": # ¨
            if char.upper:
                img.circle(pt_sg(*pts[:2:], 2), fontSize*0.1*tk, col, -tk, lt)
                img.circle(pt_sg(*pts[1::-1], 2), fontSize*0.1*tk, col, -tk, lt)
            else:
                img.circle(pt_sg(ct1, ct, 2), fontSize*0.1*tk, col, -tk, lt)
                img.circle(pt_sg(ct2, ct, 2), fontSize*0.1*tk, col, -tk, lt)
        case "47": # ̇
            if char.upper:
                img.circle(ct_sg(*pts[:2:]), fontSize*0.1*tk, col, -tk, lt)
            else:
                img.circle(ct_sg(ct1, ctd), fontSize*0.1*tk, col, -tk, lt)
        case "48": # ̆
            r = (fontSize*0.4 for _ in "00")
            if char.upper: img.ellipse(ct_sg(*pts[:2:]), r, col, tk, lt, 0, 180, an)
            else: img.ellipse(pt_sg(cth, ct, 2), r, col, tk, lt, 0, 180, an)
        case "49": # ¯
            if char.upper: LINES += [[pt_sg(*pts[1::-1], 2), pt_sg(*pts[:2:], 2)]]
            else: LINES += [[ct_sg(ct1, ctg), ct_sg(ct2, ctd)]]
        case "50": # ~
            if char.upper:
                pt1, pt2 = pt_sg(*pts[:2:], 3, 2), pt_sg(*pts[1::-1], 3, 2)
                r = (dist(pt1, ct_sg(*pts[:2:])), dist(ct_sg(*pts[:2:]), ch)/3)
                img.ellipse(pt1, r, col, tk, lt, 180, 360, an)
                img.ellipse(pt2, r, col, tk, lt, 0, 180, an)
            else:
                pt1, pt2 = ct_sg(cth, ctg), ct_sg(cth, ctd)
                r = (dist(pt1, ct_sg(cth, ct)), dist(ct_sg(*pts[:2:]), ch)/3)
                img.ellipse(pt1, r, col, tk, lt, 180, 360, an)
                img.ellipse(pt2, r, col, tk, lt, 0, 180, an)
        case "51": # '
            if char.upper: LINES += [[ct_sg(*pts[:2:]), pt_sg(ch, ct_sg(*pts[:2:]), 2)]]
            else: LINES += [[cth, ct_sg(cth, ct)]]
        case "52": # "
            if char.upper:
                pt1, pt2 = pt_sg(*pts[:2:], 5, 4), pt_sg(*pts[:2:], 4, 5)
                d = dist(pt1, pt_sg(ch, ct_sg(*pts[:2:]), 2))
            else:
                d = dist(cth, ct_sg(cth, ct))
                pt1, pt2 = ct_sg(cth, ct1), ct_sg(cth, ct2)
            LINES += [[pt1, coosCircle(pt1, d, 90+an)], [pt2, coosCircle(pt2, d, 90+an)]]
        case "53": # °
            if char.upper: img.circle(ct_sg(*pts[:2:]), fontSize*0.4, col, tk, lt)
            else: img.circle(pt_sg(cth, ct, 2), fontSize*0.4, col, tk, lt)
        ## Diacritiques souscrits ##############################
        case "60": # Cédille
            LINES += [[ct_sg(ct4, cb), pt_sg(*pts[2::], 2)]]
        case "61": # Ogonyek
            LINES += [[ct_sg(ct3, cb), pt_sg(*pts[:1:-1], 2)]]
        ## Symbols #############################################
        case "A0": ## 0
            r = (dist(ct, ct_sg(cd, ctd)), dist(ct, ch))
            img.ellipse(ct, r, col, tk, lt, angle=an)
            LINES += [[coosEllipse(ct, r, 140, an), coosEllipse(ct, r, 320, an)]]
        case "A1": ## 1
            LINES += [[ct_sg(ct1, pgh), ch], [ch, cb], [p3, p4]]
        case "A2": ## 2
            r = (dist(ct, cd), dist(cth, ch))
            img.ellipse(cth, r, col, tk, lt, 210, 400, an)
            LINES += [[coosEllipse(cth, r, 400, an), p3], [p3, p4]]
        case "A3": ## 3
            img.ellipse(cth, (dist(ct, cd), dist(cth, ch)), col, tk, lt, 220, 450, an)
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, 270, 510, an)
        case "A4": ## 4
            LINES += [[phd, ct_sg(cg, pgb)], [ct_sg(cg, pgb), ct_sg(cd, pdb)], [phd, pbd]]
        case "A5": ## 5
            p, pe = pt_sg(p1, phg, 3), pt_sg(ct, cb, 3, 2)
            LINES += [[p, p2], [p, cg]]
            img.ellipse(ct, (dist(ct, cg), dist(pe, cb)*2-dist(ct, cb)), col, tk, lt, 180, 270, an)
            img.ellipse(pe, (dist(ct, cd), dist(pe, cb)), col, tk, lt, -90, 90, an)
            img.ellipse(ct_sg(ctb, cb), (dist(ct, cg), dist(ctb, cb)/2), col, tk, lt, 90, 180, an)
        case "A6": ## 6 # FIXME 6
            img.ellipse(cth, (dist(ct, ct_sg(cd, ctd)), dist(ctb, cb)), col, tk, lt, 0, 130, an+180)
            img.ellipse(ctb, (dist(ct, ct_sg(cd, ctd)), dist(cth, ch)), col, tk, lt, angle=an)
            LINES += [[ct_sg(ct1, pgh), ct_sg(ct3, pgb)]]
        case "A7": ## 7
            LINES += [[p1, phd], [phd, cb], [ctg, cd]]
        case "A8": ## 8
            img.ellipse(cth, (dist(ct, ct_sg(cd, ctd))*0.9, dist(cth, ch)), col, tk, lt, angle=an)
            img.ellipse(ctb, (dist(ct, ct_sg(cd, ctd)), dist(ctb, cb)), col, tk, lt, angle=an)
        case "A9": ## 9 # FIXME 9
            img.ellipse(ctb, (dist(ct, ct_sg(cd, ctd)), dist(ctb, cb)), col, tk, lt, 0, 130, an)
            img.ellipse(cth, (dist(ct, ct_sg(cd, ctd)), dist(cth, ch)), col, tk, lt, angle=an)
            LINES += [[ct_sg(ct2, pdh), ct_sg(ct4, pdb)]]
        case "B0": ## .
            img.circle(cb, fontSize*0.2, col, -tk, lt)
        case "B1": ## ,
            LINES += [[cb, pt_sg(pts[2], pts[3], 5, 4)]]
        case "B2": ## :
            img.circle(cb, fontSize*0.2, col, -tk, lt)
            img.circle(ct, fontSize*0.2, col, -tk, lt)
        case "B3": ## ;
            img.circle(ct, fontSize*0.2, col, -tk, lt)
            LINES += [[ct_sg(ct4, cb), ct_sg(pbg, cb)]]
        case "B4": ## -
            LINES += [[ct_sg(cg, ctg), ct_sg(cd, ctd)]]
        case "B5": ## _
            LINES += [[p3, p4]]
        case "B6": ## !
            LINES += [[ch, ctb]]
            img.circle(cb, fontSize*0.2, col, -tk, lt)
        case "B7": ## ?
            LINES += [[ct, ctb]]
            img.ellipse(cth, (dist(ch, p1), dist(cth, ch)), col, tk, lt, 210, 450, an)
            img.circle(cb, fontSize*0.2, col, -tk, lt)
        case "B8": ## ¡
            LINES += [[cth, cb]]
            img.circle(ch, fontSize*0.2, col, -tk, lt)
        case "B9": ## ¿
            LINES += [[ct, cth]]
            img.ellipse(ctb, (dist(cb, p3), dist(ctb, cb)), col, tk, lt, 30, 270, an)
            img.circle(ch, fontSize*0.2, col, -tk, lt)
        case "C0": ## '
            LINES += [[ch, cth]]
        case "C1": ## "
            a = 3
            LINES += [[pt_sg(ch, p1, a), pt_sg(cth, pgh, a)], [pt_sg(ch, p2, a), pt_sg(cth, pdh, a)]]
        case "C2": ## ·
            img.circle(ct, fontSize*0.2, col, -tk, lt)
        case "C3": ## $
            LINES += [[ch, cb]]
            draw_char(img, "A18", ps, col, fs, tk, lt, an)
        case "C4": ## %
            LINES += [[ct2, ct3]]
            for pt in [ct1, ct4]:
                p = pt_sg(pt, ct, 5, 2)
                img.circle(p, dist(pt, p), col, tk, lt)
        case "C5": ## &
            p = pt_sg(cth, ch, 5, 2)
            r, r1, r2 = (dist(cth, ct1), dist(cth, ch)), (dist(ct1, p)*0.7, dist(p, ch)), (dist(ctb, pgb), dist(ctb, cb))
            a1, a2, a3 = 140, 420, 220
            img.ellipse(cth, r, col, tk, lt, a1, 270, an)
            img.ellipse(p, r1, col, tk, lt, 270, a2, an)
            img.ellipse(ctb, r2, col, tk, lt, -20, a3, an)
            LINES += [[coosEllipse(cth, r, a1, an), p4], [coosEllipse(p, r1, a2, an), coosEllipse(ctb, r2, a3, an)]]
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
            img.ellipse(ctd, (dist(ct, cg), dist(ct, ch)*1.2), col, tk, lt, 120, 240, an)
        case "D1": ## )
            img.ellipse(ctg, (dist(ct, cg), dist(ct, ch)*1.2), col, tk, lt, 120, 240, an+180)
        case "D2": ## [
            LINES += [[phg, phd], [phg, pbg], [pbg, pbd]]
        case "D3": ## ]
            LINES += [[phg, phd], [phd, pbd], [pbg, pbd]]
        case "D4": ## { # TODO {
            ...
        case "D5": ## } # TODO }
            ...
        case "D6": ## |
            LINES += [[ch, cb]]
        case "D7": ## @
            img.ellipse(ct, (dist(ct, cd), dist(ct, cb)), col, tk, lt, 60, 360, an)
            img.ellipse(ct, (dist(ctb, ct4), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(ctd, (dist(ctd, cd), dist(ctd, ct4)), col, tk, lt, 0, 90, an)
            LINES += [[ct2, ct4]]
        case "D8": ## #
            LINES += [[ct_sg(cg, pgh), ct_sg(cd, pdh)], [ct_sg(cg, pgb), ct_sg(cd, pdb)], [ch, ct_sg(p3, pbg)], [ct_sg(p2, phd), cb]]
        case "D9": ## ¬
            LINES += [[ct_sg(cg, ctg), ct_sg(cd, ctd)], [ct_sg(cd, ctd), ct_sg(ct4, pdb)]]
        case "E0": ## º # TODO º
            ...
        case "E1": ## ª # TODO ª
            ...
        case "E2": ## `
            LINES += [[pt_sg(p1, p2, 2), pt_sg(pdh, pgh, 2)]]
        case "E3": ## ´
            LINES += [[pt_sg(p2, p1, 2), pt_sg(pgh, pdh, 2)]]
        case "E4": ## ^
            LINES += [[pt_sg(pdh, pgh, 4), ch], [ch, pt_sg(pgh, pdh, 4)]]
        case "E5": ## ¨
            img.circle(ct_sg(phg, ct1), fontSize*0.2*tk, col, -tk, lt)
            img.circle(ct_sg(phd, ct2), fontSize*0.2*tk, col, -tk, lt)
        ########################################################
        case "F0": ## <
            LINES += [[ctd, ct3], [ct3, pbd]]
        case "F1": ## >
            LINES += [[ctg, ct4], [ct4, pbg]]
        case "F2": ## \
            LINES += [[phg, pbd]]
        ########################################################
        case "F6": ## ¦
            LINES += [[ch, ct_sg(cth, ct)], [cb, ct_sg(ctb, ct)]]
        ########################################################
        case "F8": ## ×
            LINES += [[pt_sg(ct1, ct, 2), pt_sg(ct4, ct, 2)], [pt_sg(ct2, ct, 2), pt_sg(ct3, ct, 2)]]
        case "F9": ## ÷
            LINES += [[ctg, ctd]]
            img.circle(ct_sg(cth, ct), fontSize*0.2, col, -tk, lt)
            img.circle(ct_sg(ctb, ct), fontSize*0.2, col, -tk, lt)
        case "G0": ## ’
            LINES += [[p2, ct2]]
        ## Letters #############################################
        case "A00": ## A
            LINES += [[p3, ch], [ch, p4], [ct_sg(p3, ch), ct_sg(ch, p4)]]
        case "A01": ## B
            LINES += [[p1, p3], [p3, cb], [cg, ct], [p1, ch]]
            img.ellipse(cth, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, 270, 450, an)
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, 270, 450, an)
        case "A02": ## C
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 50, 300, an)
        case "A03": ## D
            LINES += [[p1, p3], [p3, cb], [p1, ch]]
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 270, 450, an)
        case "A04": ## E
            LINES += [[p1, p3], [cg, ctd], [p3, p4], [p1, pt_sg(p2, phd, 3)]]
        case "A05": ## F
            LINES += [[p1, p3], [cg, ctd], [p1, p2]]
        case "A06": ## G
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 0, 300, an)
            LINES += [[ct, cd]]
        case "A07": ## H
            LINES += [[p1, p3], [p2, p4], [cg, cd]]
        case "A08": ## I
            LINES += [[p1, p2], [p3, p4], [ch, cb]]
        case "A09": ## J
            LINES += [[phg, p2], [p2, pdb]]
            img.ellipse(ctb, (dist(pdb, ctb), dist(ctb, cb)), col, tk, lt, 0, 135, an)
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
            img.ellipse(cth, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A16": ## Q
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, angle=an)
            LINES += [[ctb, p4]]
        case "A17": ## R
            LINES += [[p1, p3], [cg, ct], [p1, ch], [ct, p4]]
            img.ellipse(cth, [dist(ch, p2)*0.8, dist(cth, ch)], col, tk, lt, 270, 450, an)
        case "A18": ## S ## FIXME S
            img.ellipse(cth, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, 90, 300, an)
            img.ellipse(ctb, (dist(cb, p4)*0.8, dist(ctb, cb)), col, tk, lt, -90, 130, an)
        case "A19": ## T
            LINES += [[p1, p2], [ch, cb]]
        case "A20": ## U
            LINES += [[p1, pgb], [p2, pdb]]
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
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 90, 270, an)
            LINES += [[ch, cb], [ct, ct_sg(cd, ctd)], [cb, p4], [ch, p2]]
        case "A28": ## Þ
            LINES += [[p1, p3], [pgh, cth], [pgb, ctb]]
            img.ellipse(ct, (dist(ch, p2)*0.8, dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A29": ## Ð
            LINES += [[phg, pbg], [pbg, cb], [phg, ch], [cg, ct]]
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 270, 450, an)
        case "A30": ## А
            char.char = "A00"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A31": ## Б
            LINES += [[p1, p3], [p3, cb], [cg, ct], [p1, ct_sg(p2, phd)]]
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, 270, 450, an)
        case "A32": ## В
            char.char = "A01"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A33": ## Г
            LINES += [[p1, p3], [p1, p2]]
        case "A34": ## Д
            LINES += [[pgb, p3], [pdb, p4], [pgb, pdb], [phg, ct_sg(phd, p2)], [ct_sg(phd, p2), ct_sg(ct4, pdb)]]
            img.ellipse(ct_sg(p1, phg), (dist(p1, phg)/2, dist(p1, pgb)), col, tk, lt, 0, 90, an)
        case "A35": ## Е
            char.char = "A04"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A36": ## Ё
            for c in ["A35", "46"]:
                char.char = c
                draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A37": ## Ж
            LINES += [[p1, ctg], [ctg, p3], [ctg, ctd], [ch, cb], [p2, ctd], [ctd, p4]]
        case "A38": ## З
            img.ellipse(cth, (dist(ch, p2)*0.9, dist(cth, ch)), col, tk, lt, 220, 450, an)
            img.ellipse(ctb, (dist(ct, cd), dist(ctb, cb)), col, tk, lt, 270, 500, an)
        case "A39": ## И
            LINES += [[p1, p3], [p3, p2], [p2, p4]]
        case "A40": ## Й
            for c in ["A39", "48"]:
                char.char = c
                draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A41": ## К
            LINES += [[p1, p3], [cg, ctg], [ctg, p2], [ctg, p4]]
        case "A42": ## Л
            img.ellipse(p1, (dist(p1, phg), dist(p1, p3)), col, tk, lt, 0, 90, an)
            LINES += [[phg, p2], [p2, p4]]
        case "A43": ## М
            LINES += [[p3, phg], [phg, ctb], [ctb, phd], [phd, p4]]
        case "A44": ## Н
            char.char = "A07"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A45": ## О
            char.char = "A14"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A46": ## П
            LINES += [[p1, p3], [p1, p2], [p2, p4]]
        case "A47": ## Р
            char.char = "A15"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A48": ## С
            char.char = "A02"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A49": ## Т
            char.char = "A19"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A50": ## У
            LINES += [[p2, p3], [p1, ct]]
        case "A51": ## Ф
            LINES += [[ch, cb], [phg, phd], [pbg, pbd]]
            img.ellipse(ct, (dist(ct, cd), dist(ct, pt_sg(cth, ch, 2))), col, tk, lt, angle=an)
        case "A52": ## Х
            char.char = "A23"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A53": ## Ц
            LINES += [[p1, p3], [p3, p4], [ct_sg(phd, p2), ct_sg(pbd, p4)], [p4, coosCircle(p4, fontSize, 90+an)]]
        case "A54": ## Ч
            LINES += [[p2, p4], [p1, pgh], [ctd, cd]]
            img.ellipse(ct2, (dist(ct2, pgh), dist(cth, ct)), col, tk, lt, 90, 180, an)
        case "A55": ## Ш
            LINES += [[p1, p3], [p3, p4], [ch, cb], [p2, p4]]
        case "A56": ## Щ
            pt1, pt2 = ct_sg(phd, p2), ct_sg(pbd, p4)
            LINES += [[p1, p3], [p3, p4], [ct_sg(pt1, p1), ct_sg(pt2, p3)], [pt1, pt2], [p4, coosCircle(p4, fontSize, 90+an)]]
        case "A57": ## Ъ
            LINES += [[p1, phg], [phg, pbg], [ctg, ct], [pbg, cb]]
            img.ellipse(ctb, (dist(ch, p2), dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A58": ## Ы
            LINES += [[p1, p3], [cg, ctg], [p3, pbg], [p2, p4]]
            img.ellipse(ct3, (dist(ch, p2), dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A59": ## Ь
            LINES += [[p1, p3], [cg, ct], [p3, cb]]
            img.ellipse(ctb, (dist(ch, p2), dist(cth, ch)), col, tk, lt, 270, 450, an)
        case "A60": ## Э
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, 240, 490, an)
            LINES += [[ct, cd]]
        case "A61": ## Ю
            img.ellipse(ct_sg(ct, ctd), (dist(ct_sg(ct, ctd), cd), dist(ct, ch)), col, tk, lt, angle=an)
            LINES += [[p1, p3], [cg, ctg]]
        case "A62": ## Я
            LINES += [[p2, p4], [cd, ct], [p2, ch], [ct, p3]]
            img.ellipse(cth, [dist(ch, p2)*0.8, dist(cth, ch)], col, tk, lt, 90, 270, an)
        ##################
        case "A70": ## Α
            char.char = "A00"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A71": ## Β
            char.char = "A01"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A72": ## Γ
            char.char = "A33"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A73": ## Δ
            LINES += [[p3, ch], [ch, p4], [p3, p4]]
        case "A74": ## Ε
            char.char = "A04"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A75": ## Ζ
            char.char = "A25"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A76": ## Η
            char.char = "A07"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A77": ## Θ
            img.ellipse(ct, (dist(ct, cd), dist(ct, ch)), col, tk, lt, angle=an)
            LINES += [[cg, cd]]
        case "A78": ## Ι
            char.char = "A08"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A79": ## Κ
            char.char = "A41"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A80": ## Λ
            LINES += [[p3, ch], [ch, p4]]
        case "A81": ## Μ
            char.char = "A12"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A82": ## Ν
            char.char = "A13"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A83": ## Ξ
            LINES += [[p1, p2], [p3, p4], [ctg, ctd]]
        case "A84": ## Ο
            char.char = "A14"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A85": ## Π
            char.char = "A46"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A86": ## Ρ
            char.char = "A15"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A87": ## Σ
            LINES += [[p1, p2], [p3, p4], [p1, ct], [ct, p3]]
        case "A88": ## Σ
            LINES += [[p1, p2], [p2, p3], [p3, p4]]
        case "A89": ## Τ
            char.char = "A19"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A90": ## Υ
            LINES += [[p1, ct], [p2, ct], [ct, cb]]
        case "A91": ## Φ
            char.char = "A51"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A92": ## Χ
            char.char = "A23"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "A93": ## Ψ
            c, d = cth, (dist(ct, cd), dist(ct, ch))
            img.ellipse(c, d, col, tk, lt, 0, 180, an)
            LINES += [[ch, cb], [coosEllipse(c, d, 0, an), p2], [coosEllipse(c, d, 180, an), p1]]
        case "A94": ## Ω
            y, a, b = dist(ct, ch), 140, 400
            p, d = [ct[0], ct[1]-dist(ct, ch)+y], (dist(ct, cd), y)
            img.ellipse(p, d, col, tk, lt, a, b, an)
            LINES += [[p3, pbg], [coosEllipse(p, d, a, an), pbg], [coosEllipse(p, d, b, an), pbd], [pbd, p4]]
        ########################################################
        case "B00": # a
            p, r, a, a1 = pt_sg(ctb, pbg, 2), (dist(ctb, cb)/2, dist(ctb, cb)/2), 90, 270
            img.ellipse(p, r, col, tk, lt, a, a1, an)
            img.ellipse(ct_sg(ct, ctb), (dist(cb, pbd), dist(ctb, ct)*0.4), col, tk, lt, 180, 360, an)
            LINES += [[ct_sg(ctd, ct4), pbd], [coosEllipse(p, r, a, an), pt_sg(pbd, ct_sg(ctd, ct4), 10)], [coosEllipse(p, r, a1, an), pt_sg(ct_sg(ctd, ct4), pbd, 3)]]
        case "B01": # b
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[ct1, pbg]]
        case "B02": # c
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 60, 300, an)
        case "B03": # d
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[ct2, pbd]]
        case "B04": # e
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 30, angle=an)
            LINES += [[ct3, ct4]]
        case "B05": # f
            img.ellipse(ctd, (dist(ct, ctd), dist(ct, cth)), col, tk, lt, 180, 300, an)
            LINES += [[ctg, ctd], [ct, cb]]
        case "B06": # g
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(cb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 0, 150, an)
            LINES += [[ctd, pbd]]
        case "B07": # h
            img.ellipse(ctb, (dist(ct, ctg), dist(ct, ctg)), col, tk, lt, 180, 360, an)
            LINES += [[ct1, pbg], [ct4, pbd]]
        case "B08": # i
            LINES += [[pbg, pbd], [ct, cb], [ctg, ct]]
            if not char.diacr: img.circle(cth, fontSize*0.2, col, tk, lt)
        case "B09": # j
            LINES += [[ct, cb], [ctg, ct]]
            if not char.diacr: img.circle(cth, fontSize*0.2, col, tk, lt)
            img.ellipse(pbg, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 0, 90, an)
        case "B10": # k
            LINES += [[ct1, pbg], [pt_sg(ct3, ctd, 2), pbd], [ct3, ctd]]
        case "B11": # l
            LINES += [[ct1, cth], [cth, ctb]]
            img.ellipse(ct4, (dist(ctb, ct3), dist(ctb, cb)), col, tk, lt, 90, 180, an)
        case "B12": # m
            LINES += [[cg, p3], [ctb, cb], [pdb, p4]]
            img.ellipse(ct3, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, 180, 360, an)
            img.ellipse(ct4, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, 180, 360, an)
        case "B13": # n
            LINES += [[ctg, pbg], [ct4, pbd]]
            img.ellipse(ctb, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, 180, 360, an)
        case "B14": # o
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
        case "B15": # p
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[ctg, coosCircle(pbg, dist(ct, ctb), 90+an)]]
        case "B16": # q
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[ctd, coosCircle(pbd, dist(ct, ctb), 90+an)]]
        case "B17": # r
            r, a = (dist(ct4, ct3), dist(ct4, ctd)), 270
            img.ellipse(ct4, r, col, tk, lt, 180, a, an)
            LINES += [[ctg, pbg], [p3, cb], [ct_sg(cg, ctg), ctg], [ctd, pt_sg(ctd, ct4, 2)]]
        case "B18": # s
            pt1, pt2 = ct_sg(ct, ctb), ct_sg(cb, ctb)
            r = (dist(ct, ctd), dist(pt1, ct))
            img.ellipse(pt1, (dist(ct, ctd)*0.9, dist(pt1, ct)), col, tk, lt, 90, 330, an)
            img.ellipse(pt2, (dist(ct, ctd), dist(pt1, ct)), col, tk, lt, -90, 160, an)
        case "B19": # t
            LINES += [[cth, ctb], [ctg, ctd]]
            img.ellipse(ct4, (dist(ct4, ctb), dist(ct4, pbd)), col, tk, lt, 90, 180, an)
        case "B20": # u
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 0, 180, an)
            LINES += [[ctg, ct3], [ctd, pbd]]
        case "B21": # v
            LINES += [[ctg, cb], [ctd, cb]]
        case "B22": # w
            LINES += [[cg, pbg], [pbg, ct_sg(ctb, ct)], [ct_sg(ctb, ct), pbd], [pbd, cd]]
        case "B23": # x
            LINES += [[ctg, pbd], [ctd, pbg]]
        case "B24": # y
            LINES += [[ctg, cb], [ctd, cb]]
            img.ellipse(pbg, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 0, 90, an)
        case "B25": # z
            LINES += [[ctg, ctd], [ctd, pbg], [pbg, pbd]]
        case "B26": # æ # FIXME æ
            LINES += [[ct3, ct4], [ct, cb]]
            r = (dist(ctg, ct), dist(ctb, ct))
            img.ellipse(ct3, r, col, tk, lt, 270, 360, an)
            img.ellipse(ctb, r, col, tk, lt, 270, 360, an)
            img.ellipse(ct4, r, col, tk, lt, 90, 180, an)
            img.ellipse(ctb, r, col, tk, lt, 90, 180, an)
        case "B27": # œ # FIXME œ
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 30, angle=an)
            LINES += [[ctb, ct4], [ct, cb]]
        case "B28": # þ
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            LINES += [[ct1, coosCircle(pbg, dist(ct, ctb), 90+an)]]
        case "B29": # ð
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(ct3, (dist(ct, cd), dist(ct, cb)), col, tk, lt, 270, 360, an)
            LINES += [[pt_sg(ctg, ct1, 2), ct2]]
        case "B30": # а
            LINES += [[pbg, ct], [ct, pbd], [ct_sg(pbg, ct), ct_sg(ct, pbd)]]
        case "B31": # б
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, angle=an)
            p, p1 = ctb, ct_sg(ch, phd)
            r, r1 = (dist(ct, ctg), dist(ctb, cth)), (dist(ct, ctg), dist(ch, cth))
            a, a1 = 270, 90
            img.ellipse(p, r, col, tk, lt, 180, a, an)
            img.ellipse(p1, r1, col, tk, lt, 60, a1, an)
            LINES += [[coosEllipse(p, r, a, an), coosEllipse(p1, r1, a1, an)]]
        case "B32": # в
            LINES += [[ctg, pbg], [ct3, ctb], [ctg, ct], [pbg, cb]]
            img.ellipse(ct_sg(ctb, ct), (dist(ct, ctd)*0.8, dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
            img.ellipse(ct_sg(ctb, cb), (dist(ct, ctd), dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B33": # г
            LINES += [[ctg, pbg], [ctg, ctd]]
        case "B34": # д
            LINES += [[ct_sg(ct3, pbg), pbg], [ct_sg(ct4, pbd), pbd], [ct_sg(ct3, pbg), ct_sg(ct4, pbd)], [pt_sg(ct, ctg, 2), ct_sg(ct, ctd)], [ct_sg(ct, ctd), ct_sg(ctb, pbd)]]
            img.ellipse(pt_sg(ctg, ct, 2), (dist(pt_sg(ctg, ct, 2), pt_sg(ct, ctg, 2)), dist(ct, ct_sg(ctb, cb))), col, tk, lt, 0, 90, an)
        case "B35": # е
            LINES += [[ctg, ctd], [ctg, pbg], [ct3, ct_sg(ctb, ct4)], [pbg, pbd]]
        case "B36": # ё
            for c in ["B35", "46"]:
                char.char = c
                draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "B37": # ж
            pt1, pt2 = ct_sg(ct3, ctb), ct_sg(ct4, ctb)
            LINES += [[ctg, pt1], [pt1, pt2], [pt1, pbg], [ct, cb], [ctd, pt2], [pt2, pbd]]
        case "B38": # з
            img.ellipse(ct_sg(ct, ctb), (dist(ct, ctd)*0.9, dist(ct, ctb)/2), col, tk, lt, 220, 450, an)
            img.ellipse(ct_sg(cb, ctb), (dist(ct, ctd), dist(ctb, cb)/2), col, tk, lt, 270, 500, an)
        case "B39": # и
            LINES += [[ctg, pbg], [ctd, pbg], [ctd, pbd]]
        case "B40": # й
            for c in ["B39", "48"]:
                char.char = c
                draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "B41": # к
            LINES += [[ctg, pbg], [ct3, ctb], [ctb, ctd], [ctb, pbd]]
        case "B42": # л
            img.ellipse(ctg, (dist(ctg, ct_sg(ctg, ct)), dist(ct, cb)), col, tk, lt, 0, 90, an)
            LINES += [[ct_sg(ctg, ct), ctd], [ctd, pbd]]
        case "B43": # м
            LINES += [[pbg, ct_sg(ctg, ct)], [ct_sg(ctg, ct), ct_sg(ctb, cb)], [ct_sg(ctb, cb), ct_sg(ctd, ct)], [ct_sg(ctd, ct), pbd]]
        case "B44": # н
            LINES += [[ctg, pbg], [ct3, ct4], [ctd, pbd]]
        case "B45": # о
            char.char = "B14"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "B46": # п
            LINES += [[ctg, pbg], [ctg, ctd], [ctd, pbd]]
        case "B47": # р
            LINES += [[ctg, pbg], [ct3, ctb], [ctg, ct]]
            img.ellipse(ct_sg(ctb, ct), (dist(ct, ctd)*0.8, dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B48": # с
            img.ellipse(ctb, (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 60, 300, an)
        case "B49": # т
            LINES += [[ct, cb], [ctg, ctd]]
        case "B50": # у
            char.char = "B24"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "B51": # ф
            LINES += [[cth, coosCircle(cb, dist(ct, cth), 90+an)]]
            img.ellipse(ct_sg(ct3, ctb), (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 65, 295, an)
            img.ellipse(ct_sg(ct4, ctb), (dist(cb, pbg), dist(ctb, cb)), col, tk, lt, 245, 475, an)
        case "B52": # х
            LINES += [[ctg, pbd], [ctd, pbg]]
        case "B53": # ц
            LINES += [[ctg, pbg], [pbg, pbd], [ct_sg(ctd, ct), ct_sg(pbd, cb)], [pbd, coosCircle(pbd, fontSize*0.5, 90+an)]]
        case "B54": # ч
            LINES += [[ctd, pbd], [ctg, ct_sg(ctg, ct3)], [ct_sg(ctb, ct4), ct4]]
            pt = ct_sg(ctd, ctb)
            img.ellipse(pt, (dist(pt, ct_sg(ctg, ct3)), dist(ctd, ct4)/2), col, tk, lt, 90, 180, an)
        case "B55": # ш
            LINES += [[ctg, pbg], [pbg, pbd], [ct, cb], [ctd, pbd]]
        case "B56": # щ
            pt1, pt2 = ct_sg(ctd, ct), ct_sg(pbd, cb)
            LINES += [[ctg, pbg], [ct_sg(ctg, pt1), ct_sg(pbg, pt2)], [pbg, pbd], [pt1, pt2], [pbd, coosCircle(pbd, fontSize*0.5, 90+an)]]
        case "B57": # ъ
            LINES += [[ctg, ct_sg(ctg, ct)], [ct_sg(ctg, ct), ct_sg(pbg, cb)], [ct_sg(pbg, cb), cb], [ct_sg(ct3, ctb), ctb]]
            img.ellipse(ct_sg(ctb, cb), (dist(ct, ctd), dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B58": # ы
            LINES += [[ctg, pbg], [ct3, ctb], [ctd, pbd], [pbg, cb]]
            img.ellipse(ct_sg(ctb, cb), (dist(ct, ctd)*0.7, dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B59": # ь
            LINES += [[ctg, pbg], [ct3, ctb], [pbg, cb]]
            img.ellipse(ct_sg(ctb, cb), (dist(ct, ctd), dist(ct, ctb)/2), col, tk, lt, -90, 90, an)
        case "B60": # э
            img.ellipse(ctb, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, 240, 490, an)
            LINES += [[ctb, ct4]]
        case "B61": # ю
            p = pt_sg(ctb, ct4, 2)
            r = (dist(p, ct4), dist(ct, ctb))
            img.ellipse(p, r, col, tk, lt, angle=an)
            LINES += [[ctg, pbg], [ct3, coosEllipse(p, r, 180, an)]]
        case "B62": # я
            LINES += [[ctd, pbd], [ct4, ctb], [ctd, ct], [ctb, pbg]]
            img.ellipse(ct_sg(ctb, ct), (dist(ct, ctd)*0.8, dist(ct, ctb)/2), col, tk, lt, 90, 270, an)
        #################
        case "B70": # α
            p = pt_sg(ctb, pgb, 2)
            img.ellipse(p, (dist(ctb, p), dist(ctb, cb)), col, tk, lt, angle=an)
            img.ellipse(pt_sg(ctb, pdb, 2), (dist(ctb, p), dist(ctb, cb)), col, tk, lt, 120, 240, angle)
        case "B71": # β
            LINES += [[coosCircle(pbg, dist(cb, ct_sg(*pts[2::])), 90+an), ctg]]
            img.ellipse(ct, (dist(ct, ctg), dist(cth, ct)), col, tk, lt, 180, 270, an)
            img.ellipse(ct, (dist(ct, ctg)*0.7, dist(cth, ct)), col, tk, lt, 270, 360, an)
            img.ellipse(ct, (dist(ct, ctg)*0.7, dist(cth, ct)*0.6), col, tk, lt, 0, 90, an)
            img.ellipse(ctb, (dist(ct, ctg), dist(ctb, ct)*0.6), col, tk, lt, 270, 360, an)
            img.ellipse(ctb, (dist(ct, ctg), dist(ctb, ct)), col, tk, lt, 0, 120, an)
        case "B72": # γ
            rs = (dist(cb, pbg), dist(cb, ct))
            img.ellipse(pbg, rs, col, tk, lt, -70, -10, an)
            img.ellipse(pbd, rs, col, tk, lt, 190, 250, an)
            img.ellipse(cb, (dist(cb, pbg)*0.1, dist(cb, coosEllipse(pbg, (dist(cb, pbg), dist(cb, ct)), -10, an))), col, tk, lt, 0, 360, an)
        case "B73": # δ
            p, rs = ctb, (dist(cb, pbg), dist(ctb, cb))
            img.ellipse(p, rs, col, tk, lt, angle=an)
            LINES += [[ct_sg(ct2, phd), ct1], [ct1, coosEllipse(p, rs, -60, an)]]
        case "B74": # ε
            rs = (dist(cb, pbg), dist(cb, ctb)/2)
            img.ellipse(ct_sg(ct, ctb), rs, col, tk, lt, 90, 310, an)
            img.ellipse(ct_sg(cb, ctb), rs, col, tk, lt, 40, 270, an)
            LINES += [[ctb, ct_sg(ctb, ct4)]]
        case "B75": # ζ
            A, B, d = 75, 210, dist(p4, pts[-1])/2
            p, rs, a = ctb, (dist(ct, ctg), dist(ctb, ct)), an+20
            p2, rs2 = pbd, (d*0.7, d*0.5)
            img.ellipse(p, rs, col, tk, lt, A, B, a)
            img.ellipse(p2, rs2, col, tk, lt, -90, 120, an)
            LINES += [[ct1,  ct2], [ct2, coosEllipse(p, rs, B, a)], [coosEllipse(p, rs, A, a), coosEllipse(p2, rs2, 270, an)]]
        case "B76": # η
            LINES += [[ctg, pbg], [ct4, coosCircle(pbd, dist(p4, pts[-1]), 90+an)]]
            img.ellipse(ctb, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, 180, 360, an)
        case "B77": # θ
            p = ct_sg(ct, ctb)
            rs = (dist(ct, ctg), dist(p, cb))
            img.ellipse(p, rs, col, tk, lt, angle=an)
            LINES += [[coosEllipse(p, rs, i, an) for i in (0, 180)]]
        case "B78": # ι
            img.ellipse(ctd, (dist(ct, ctd), dist(ct, cb)), col, tk, lt, 90, 180, an)
        case "B79": # κ
            p = pt_sg(ct3, ctb, 2)
            LINES += [[ctg, pbg], [ct3, p], [p, ctd], [p, pbd]]
        case "B80": # λ
            l = [ct1, pbd]
            LINES += [l, [ct_sg(*l), pbg]]
        case "B81": # μ
            img.ellipse(ctb, (dist(ct, ctd), dist(ct, ctb)), col, tk, lt, 0, 180, an)
            LINES += [[ctg, coosCircle(pbg, dist(p4, pts[-1]), 90+an)], [ctd, pbd]]
        case "B82": # ν
            img.ellipse(pbg, (dist(cb, pbg), dist(cb, ct)), col, tk, lt, -70, 0, an)
            LINES += [[cb, ctd]]
        case "B83": # ξ # TODO ξ
            ...
        case "B84": # ο
            char.char = "B14"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        case "B85": # π
            char.char = "B46"
            draw_char(img, char, pts, col, fs, tk, lt, an, False)
        ########################################################
        case "A000": ...
    #################################################
        case _:
            draw_char(img, "00", pts, col, fs, tk, lt, an, False)
    for a, b in LINES: img.line(a, b, col, tk, lt)
    #################################################
    if help:
        d = 3
        img.circle(pts[0], d*2, COL.compl(COL.help), 0)
        for p in pts[:-1:]: img.circle(p, d, COL.help, 0)
        t = str(char).replace(":", "\n")
        while "(" in t:
            t = t[:t.index("("):]+t[1+t.index(")")::]
        img.text(t, pts[0], COL.help, fontSize=3, centered=False)
    return ##########################################