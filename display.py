import math

#eyeleft,eyeright,sun은 길이3의 배열
def caldisplay(eyeleft,eyeright,sun):
    #눈중점좌표 계산
    eyeforcal = [0,0,0] #x,y,z
    for i in range(3):
        eyeforcal[i]=(eyeleft[i]+eyeright[i])/2
    #디스플레이 3차원좌표
    display3D= [0,0,0]
    #최종 디스플레이 퍼센트 = result, max_x는 디스플레이 계산식의 A, max_y는 디스플레이 계산식의 B 나머지는 동일
    result = [0,0]
    #e = sun[0]
    #f = sun[1]
    #g = sun[2]
    max_x = 950
    max_y = 540
    e,f,g = -3,0,3**(1/2)
    a = eyeforcal[0]
    b = eyeforcal[1]
    c = eyeforcal[2]
    #a=900
    #b=0
    #c=0
    # 디스플레이 3차원좌표 계산식
    display3D = [(c*e-a*g)*math.cos((math.pi)/3)/(e*math.sin((math.pi)/3)-g*math.cos((math.pi)/3)),((c*f-b*g)*math.cos((math.pi)/3)+(b*e-a*f)*math.sin((math.pi)/3))/(e*math.sin((math.pi)/3)-g*math.cos((math.pi)/3)),((c*e-a*g)*math.sin((math.pi)/3))/(e*math.sin((math.pi)/3)-g*math.cos((math.pi)/3))] 
    print(display3D)
    # 디스플레이 퍼센트 계산식
    result = [(display3D[1]+max_x/2)/max_x*100,(max_y-display3D[2]/math.sin(math.pi/3))/max_y*100] # y%, x%
    print("%y, %x",result)
    return result

if __name__ == "__main__":
    caldisplay([0,0,0],[0,0,0],[0,0,0])