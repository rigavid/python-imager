import math, numpy as np

type numero = float | int
type point = list[numero]

def decoupe(numb:numero) -> float:
    '''Float from complex'''
    return float(str(numb).split("j")[0].replace("(", "").replace(")", ""))

def n_entre(n:numero, mi:numero, ma:numero) -> bool:
    '''Is number between min and max'''
    return mi if n < mi else ma if n > ma else n

def ct_sg(pt1:point, pt2:point) -> point:
    '''Get the center of a segment'''
    return [(pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2]

def ct_cr(p1:point, p2:point, p3:point, p4:point) -> point:
    '''Get the center of a square'''
    return ct_sg(ct_sg(p1, p2), ct_sg(p3, p4))

def pt_sg(p1:point, p2:point, m1:numero=1, m2:numero=1) -> point:
    '''Get a point in a segment'''
    return ((p1[n] * m1 + p2[n] * m2) / (m1+m2) for n in [0, 1])

def cts(pts:list[point]) -> list[point]:
    '''Get ch, cb, cg, cd'''
    return [ct_sg(pts[0], pts[1]), ct_sg(pts[2], pts[3]), ct_sg(pts[0], pts[2]), ct_sg(pts[1], pts[3])]

def coosCercle(ct:point, rayon:numero, angle:numero) -> point:
    '''Get a point on a circle's line'''
    return [ct[0] + decoupe(str(math.cos(math.radians(angle)))) * rayon, ct[1] + decoupe(str(math.sin(math.radians(angle)))) * rayon]

def coosEllipse(ct:point, rayons:list[numero], angle:numero) -> point:
    '''Get a point on an ellipse's line'''
    p1, p2 = coosCercle(ct, min(rayons), angle), coosCercle(ct, max(rayons), angle)
    return (p1[0] - (p1[0] - p2[0]), p1[1]) if rayons[0]<rayons[1] else (p1[0], p1[1] - (p1[1] - p2[1]))

def diff(n1:numero, n2:numero) -> numero:
    '''Calcule la différence entre n1 et n2'''
    return abs(n1-n2)

def racine_carree(n:numero) -> float:
    '''Get square root'''
    return decoupe(math.sqrt(n))

def dist(p1:point, p2:point) -> float:
    '''Calcule la distance entre p1 et p2'''
    return racine_carree(diff(p1[0], p2[0])**2 + diff(p1[1], p2[1])**2)

def angleEntrePoints(p1:point, p2:point) -> float:
    '''Calcule l'angle entre p1 et p2'''
    return math.degrees(math.atan2(diff(p1[1], p2[1]), diff(p1[0], p2[0])))

def equation_2eme_degre(a:numero, b:numero, c:numero):
    try: y1 = (-b + racine_carree(b**2 - 4*a*c)) / (2*a)
    except: y1 = 'r'
    try: y2 = (-b - racine_carree(b**2 - 4*a*c)) / (2*a)
    except: y2 = 'r'
    return None if y1 == 'r' and y2 == 'r' else y2 if y1 == 'r' else y1 if y2 == 'r' else y1, y2

def oppose(n:numero) -> numero:
    ''' Donne la valeur opposée de n'''
    return(0 - n)

def moyenne(elementA:numero, elementB:numero, mult_elementA:numero=1, mult_elementB:numero=1) -> numero:
    '''Get the moyenne'''
    return ((elementA * mult_elementA) + (elementB * mult_elementB)) / (mult_elementA + mult_elementB)

def clicked_in(pos:point, boutton:list[point]) -> bool:
    return pos[0] >= boutton[0][0] and pos[0] <= boutton[1][0] and pos[1] >= boutton[0][1] and pos[1] <= boutton[1][1]