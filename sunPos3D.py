import math

alpha, beta = 1, 500 # 나중에 바꿀곳

a = 4608 / 2
b = 2592 / 2

theta0 = math.pi / 180 * 51
pi0 = math.pi / 180 * (67/2)

theta1 = math.atan(alpha * math.tan(theta0) / a)
pi1 = math.atan(beta * math.tan(pi0) / b)

print("<", -a/math.tan(theta0),",", a*math.tan(theta1)/math.tan(theta0), ",", b*math.tan(pi1)/math.tan(pi0), ">")