try: from pyimager.resolution import resolution as RES
except: from resolution import resolution as RES
try: from pyimager.colourors import colour as COL
except: from colors import colour as COL
try: from pyimager.calculs import *
except: from calculs import *
screen = RES.resolution
long, haut = screen
hg = [0, 0]
hd = [long, 0]
bg = [0, haut]
bd = [long, haut]
ct = [round(long/2), round(haut/2)]
p1 = [round((long-haut)/2), 0]
p2 = [round((long-haut)/2)+haut, 0]
p3 = [round((long-haut)/2), haut]
p4 = [round((long-haut)/2)+haut, haut]
cg = ct_sg(p1, p3)
cd = ct_sg(p2, p4)
ch = ct_sg(p1, p2)
cb = ct_sg(p3, p4)
ct = ct_cr(p1, p2, p3, p4)