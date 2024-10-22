import math

def changeX(k):
    return k * 3.4 * math.tan(25.67*math.pi/180) / 320
def changeY(k):
    return k * 3.4 * math.tan(19.8254*math.pi/180) / 320

def runEyePos3D(cam0x,cam0y,cam1x,cam1y):
    
    b, a, e, d = changeX(cam0x),changeY(cam0y),changeX(cam1x),cam1y #나중에 바꿀곳
    l = 3.4 #카메라 초점거리

    if e==0:
        e=1
    if b==0:
        b=1

    theta = math.atan(b/l)
    pi = math.atan(e/l)
    #theta = math.pi / 4
    #pi = math.pi / 4

    M = 100

    x = 2*((M*math.tan(pi))/(math.tan(theta) + math.tan(pi))) / math.tan(pi)
    y = M*(math.tan(theta) - math.tan(pi))/(math.tan(theta) + math.tan(pi))
    z = 2*a*M / (l*(math.tan(theta) + math.tan(pi)))

    print("x:", x)
    print("y:", y)
    print("z:", z)
    return([x,y,x])