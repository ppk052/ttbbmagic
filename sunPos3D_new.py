import math

F = 2.5 #초점거리
def changeX(k): 
    return k * F * math.tan(27*math.pi/180) / 320
def changeY(k):
    return k * F * math.tan(20.5*math.pi/180) / 240

def runSunPos3D(cam0x,cam0y,cam1x,cam1y):
    A, B, C, D = changeX(cam0x),changeY(cam0y),changeX(cam1x),changeY(cam1y) 

    M = 150

    ac = A-C
    if ac == 0:
        x = F*M / A
    else:
        x = 2*F*M / (A-C) 
    y = M-(A*x / F)
    z = -(B+D) * x / (2*F)

    print("#############sunPos###############")
    print("A:", A)
    print("B:", B)
    print("C:", C)
    print("D:", D)
    print("sx:", x)
    print("sy:", y)
    print("sz:", z)
    print("###################################")
    return([x,y,z])