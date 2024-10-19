import math, numpy as np

def decoupe(numb):
    '''Float from complex'''
    return float(str(numb).split("j")[0].replace("(", "").replace(")", ""))

def n_entre(n, mi, ma) -> bool:
    '''Is number between min and max'''
    return mi if n < mi else ma if n > ma else n

def ct_sg(pt1, pt2):
    '''Get the center of a segment'''
    return ((pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2)

def ct_cr(p1, p2, p3, p4):
    '''Get the center of a square'''
    return ct_sg(ct_sg(p1, p2), ct_sg(p3, p4))

def pt_sg(p1, p2, m1=1, m2=1):
    '''Get a point in a segment'''
    return ((p1[n] * m1 + p2[n] * m2) / (m1+m2) for n in [0, 1])

def cts(pts) -> list[list[int | float]]:
    '''Get ch, cb, cg, cd'''
    return [ct_sg(pts[0], pts[1]), ct_sg(pts[2], pts[3]), ct_sg(pts[0], pts[2]), ct_sg(pts[1], pts[3])]

def coosCercle(ct, rayon:int | float, angle) -> list[int | float]:
    '''Get a point on a circle's line'''
    return [ct[0] + decoupe(str(math.cos(math.radians(angle)))) * rayon, ct[1] + decoupe(str(math.sin(math.radians(angle)))) * rayon]

def coosEllipse(ct, rayons, angle) -> list[int | float]:
    '''Get a point on an ellipse's line'''
    p1, p2 = coosCercle(ct, min(rayons), angle), coosCercle(ct, max(rayons), angle)
    return (p1[0] - (p1[0] - p2[0]), p1[1]) if rayons[0]<rayons[1] else (p1[0], p1[1] - (p1[1] - p2[1]))

def diff(n1, n2) -> float | int:
    '''Calcule la différence entre n1 et n2'''
    return abs(n1-n2)

def racine_carree(n) -> float:
    '''Get square root'''
    return decoupe(math.sqrt(n))

def dist(p1, p2) -> float:
    '''Calcule la distance entre p1 et p2'''
    return racine_carree(diff(p1[0], p2[0])**2 + diff(p1[1], p2[1])**2)

def angleEntrePoints(p1, p2) -> float:
    '''Calcule l'angle entre p1 et p2'''
    return math.degrees(math.atan2(diff(p1[1], p2[1]), diff(p1[0], p2[0])))

def equation_2eme_degre(a, b, c):
    try: y1 = (-b + racine_carree(b**2 - 4*a*c)) / (2*a)
    except: y1 = 'r'
    try: y2 = (-b - racine_carree(b**2 - 4*a*c)) / (2*a)
    except: y2 = 'r'
    return None if y1 == 'r' and y2 == 'r' else y2 if y1 == 'r' else y1 if y2 == 'r' else y1, y2

def oppose(n):
    ''' Donne la valeur opposée de n'''
    return(0 - n)

def moyenne(elementA, elementB, mult_elementA=1, mult_elementB=1) -> float | int:
    '''Get the moyenne'''
    return ((elementA * mult_elementA) + (elementB * mult_elementB)) / (mult_elementA + mult_elementB)

def clicked_in(pos, boutton):
    return pos[0] >= boutton[0][0] and pos[0] <= boutton[1][0] and pos[1] >= boutton[0][1] and pos[1] <= boutton[1][1]