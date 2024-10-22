import math

#eyeleft,eyeright,sun은 길이3의 배열
def caldisplay(eyeleft,eyeright,sun):
    #눈중점좌표 계산
    eyeforcal = [0,0,0]
    for i in range(3):
        eyeforcal[i]=(eyeleft[i]+eyeright[i])/2
    #디스플레이 3차원좌표
    display3D= [0,0,0]
    #최종 디스플레이 퍼센트 = result, max_x는 디스플레이 계산식의 A, max_y는 디스플레이 계산식의 B 나머지는 동일
    result = [0,0]
    max_x = 500
    max_y = 200 
    e = sun[0]
    f = sun[1]
    g = sun[2]
    a = eyeforcal[0]
    b = eyeforcal[1]
    c = eyeforcal[2]
    # 디스플레이 3차원좌표 계산식
    display3D = [(c*e-a*g)*math.cos(math.pi/3)/(e*math.sin(math.pi/3)-g*math.cos(math.pi/3)),((c*f-b*g)*math.cos(math.pi/3)+(b*e-a*f)*math.sin(math.pi/3))/(e*math.sin(math.pi/3)-g*math.cos(math.pi/3)),(c*e-a*g)*math.sin(math.pi/3)/(e*math.sin(math.pi/3)-g*math.cos(math.pi/3))] 
    print(display3D)
    # 디스플레이 퍼센트 계산식
    result = [(display3D[0]+max_x/2)/max_x*100,(max_y-display3D[1]/math.sin(math.pi/3))/max_y*100] # x%, y%
    return result