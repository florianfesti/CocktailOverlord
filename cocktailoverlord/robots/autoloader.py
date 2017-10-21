#!/usr/bin/python3

from robots.robot import Robot

class AutoLoader(Robot):

    positions = [
        (-187, -2, -188, -170), #  0 l
        (-165, -2, -160, -170), #  1 u
        (-153, -2, -148, -170), #  2 l
        (-135, -2, -125, -170), #  3 u
        (-127, -2, -125, -170), #  4 l
        (-120, -2, -125, -170), #  5 u
        (-100, -2, -102, -170), #  6 l
        ( -90, -2,  -95, -170), #  7 u
        ( -63, -2,  -59, -170), #  8 l
        ( -45, -2,  -40, -170), #  9 u
        ( -36, -2,  -34, -170), # 10 l      
        ( -28, -2,  -33, -170), # 11 u
        ( -10, -2,  -12, -170), # 12 l      
        (  15, -2,   23, -170), # 13 u
        (  30, -2,   35, -170), # 14 l
        
    ]

    def __init__(self, port=None):
        super().__init__(port)
        self.speedx = 10000
        self.speedy = 5000

    def gcode(self, pos, amount, reserve):
        xo,yo, xi, yi = self.positions[pos]
        sx, sy = self.speedx, self.speedy
        time = amount / 10. # XXX use reserve
        return b"""
g1 y %i f %i
g1 x %i f %i
g1 x %i y %i f %i
g4 P %.2f
g1 x %i y %i f %i
""" % (yo, sy,
       xo, sx,
       xi, yi, sy,
       time,
       xo, yo, sy)

if __name__ == "__main__":
    al = AutoLoader("/dev/ttyUSB0")
    al.send(b'\n$H\n')
    #for i in (0, 1, 2, 14,):
    #    al.send(al.gcode(i, 2.5))
    #print(al.gcode(9, 2.5))
    al.wait()
