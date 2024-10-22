import math

def runEyePos3D(cam0x,cam0y,cam1x,cam1y):
    
    b, a, e, d = cam0x,cam0y,cam1x,cam1y #나중에 바꿀곳
    l = 3.4 #카메라 초점거리

    if e==0:
        e=1
    if b==0:
        b=1

    theta = b/l
    pi = e/l
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