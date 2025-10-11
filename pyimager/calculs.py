import math

type number = float | int
type point = list[number] | tuple[number]

def is_between(n:number, mi:number, ma:number) -> bool:
    '''Is number between min and max'''
    return mi if n < mi else ma if n > ma else n

def ct_sg(p1:point, p2:point) -> point:
    '''Get the center of a segment'''
    return [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2]

def ct_cr(p1:point, p2:point, p3:point, p4:point) -> point:
    '''Get the center of a parallelogram'''
    return ct_sg(ct_sg(p1, p2), ct_sg(p3, p4))

def pt_sg(p1:point, p2:point, m1:number=1, m2:number=1) -> point:
    '''Get a point in a segment'''
    return [(p1[n] * m1 + p2[n] * m2) / (m1+m2) for n in [0, 1]]

def cts(pts:list[point]) -> list[point]:
    '''Get ch, cb, cg, cd'''
    return [ct_sg(pts[0], pts[1]), ct_sg(pts[2], pts[3]), ct_sg(pts[0], pts[2]), ct_sg(pts[1], pts[3])]

def coosCircle(ct:point, radius:number, angle:number) -> point:
    '''Get a point on a circle's line'''
    return [ct[0] + math.cos(math.radians(angle)).real * radius, ct[1] + math.sin(math.radians(angle)).real * radius]

def coosEllipse(ct:point, radiuses:list[number], angle:number, rotation:number) -> point:
    '''Get a point on an ellipse's line'''
    p1, p2 = coosCircle(ct, max(radiuses), angle), coosCircle(ct, min(radiuses), angle)
    pt = (p1[0] - (p1[0] - p2[0]), p1[1]) if radiuses[0]<radiuses[1] else (p1[0], p1[1] - (p1[1] - p2[1]))
    return coosCircle(ct, dist(ct, pt), angleInterPoints(ct, pt)+rotation)

def diff(n1:number, n2:number) -> number:
    '''Calculate the difference between n1 and n2'''
    return abs(n1-n2)

def square_root(n:number) -> float:
    '''Get the square root'''
    return math.sqrt(n).real

def dist(p1:point, p2:point) -> float:
    '''Calculates distance from p1 to p2\nIf you have a TypeError, maybe you should use diff() instead of dist()'''
    return square_root(diff(p1[0], p2[0])**2 + diff(p1[1], p2[1])**2)

def angleInterPoints(p1:point, p2:point) -> float:
    '''Calculate the angle between p1 and p2'''
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

def equation2dDegre(a:number, b:number, c:number):
    '''a, b², 2c'''
    try: y1 = (-b + square_root(b**2 - 4*a*c)) / (2*a)
    except: y1 = 'r'
    try: y2 = (-b - square_root(b**2 - 4*a*c)) / (2*a)
    except: y2 = 'r'
    return None if y1 == 'r' and y2 == 'r' else y2 if y1 == 'r' else y1 if y2 == 'r' else y1, y2

def average(elementA:number, elementB:number, mult_elementA:number=1, mult_elementB:number=1) -> number:
    '''Get the average from values'''
    return ((elementA * mult_elementA) + (elementB * mult_elementB)) / (mult_elementA + mult_elementB)

def clicked_in(pos:point, button:list[point]) -> bool:
    """ Is pos[x, y] in button[[x, y]-[x, y]] """
    (x1, y1), (x2, y2) = button
    return min(x1, x2) <= pos[0] <= max(x1, x2) and min(y1, y2) <= pos[1] <= max(y1, y2)