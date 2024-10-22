import math

F = 3.4 #초점거리
def changeX(k):
    return k * F * math.tan(25.67*math.pi/180) / 320
def changeY(k):
    return k * F * math.tan(19.8254*math.pi/180) / 320

def runEyePos3D(cam0x,cam0y,cam1x,cam1y):
    A, B, C, D = changeX(cam0x),changeY(cam0y),changeX(cam1x),changeY(cam1y) 

    M = 100

    x = 2*F*M / (A+C) 
    y = M - (2*M*A / (A+C))
    z = M*(B+D) / (A+C)

    print("x:", x)
    print("y:", y)
    print("z:", z)
    return([x,y,x])