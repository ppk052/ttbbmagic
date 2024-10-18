import math

b, a, e, d = 1,1,1,1 #나중에 바꿀곳
l = 0.2 #나중에 바꿀곳

#theta = b/l
#pi = e/l
theta = math.pi / 4
pi = math.pi / 4

M = 1

x = 2*((M*math.tan(pi))/(math.tan(theta) + math.tan(pi))) / math.tan(pi)
y = M*(math.tan(theta) - math.tan(pi))/(math.tan(theta) + math.tan(pi))
z = 2*a*M / (l*(math.tan(theta) + math.tan(pi)))

print("x:", x)
print("y:", y)
print("z:", z)
print(math.tan(theta))
print(math.tan(pi))