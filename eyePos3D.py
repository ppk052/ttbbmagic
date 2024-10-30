import math

F = 3.6 #초점거리
def changeX(k):
    return k * F * math.tan(25.67*math.pi/180) / 320
def changeY(k):
    return k * F * math.tan(19.8254*math.pi/180) / 240

def runEyePos3D(cam0x,cam0y,cam1x,cam1y):
    A, B, C, D = changeX(cam0x),changeY(cam0y),changeX(cam1x),changeY(cam1y) 

    M = 200

    ac = A-C
    if ac == 0:
        x = F*M / A
    else:
        x = 2*F*M / (A-C) 
    y = (A*x / F) - M
    z = (B+D) * x / (2*F)

    print("#############eyePos###############")
    print("A:", A)
    print("B:", B)
    print("C:", C)
    print("D:", D)
    print("x:", x)
    print("y:", y)
    print("z:", z)
    print("###################################")
    return([x,y,z])