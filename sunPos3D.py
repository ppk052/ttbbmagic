import math

def runSunPos3D(alpha, beta):
    a = 4608 / 2
    b = 2592 / 2

    theta0 = math.pi / 180 * 51
    pi0 = math.pi / 180 * (67/2)

    theta1 = math.atan(alpha * math.tan(theta0) / a)
    pi1 = math.atan(beta * math.tan(pi0) / b)
    resultx = -a/math.tan(theta0)
    resulty = a*math.tan(theta1)/math.tan(theta0)
    resultz = b*math.tan(pi1)/math.tan(pi0)
    print("<", -a/math.tan(theta0),",", a*math.tan(theta1)/math.tan(theta0), ",", b*math.tan(pi1)/math.tan(pi0), ">")
    return [resultx,resulty,resultz]