import random
import time
import queue
import threading
import Simulation2
deal_queue_len=100
wait_queue_num=2
def generator(num,lambd1,lambd2):
    on_min = 0.1
    off_min = 0.2
    flag = True
    n=0
    src=[]
    while (n<500000):
        if (flag == True):  # on周期
            on_time = random.expovariate(lambd1)#获得lambda=lambd1的指数分布on时间
            if (on_min > on_time):
                on_time = on_min#如果小于最小on时间取on_min
            #print(on_time)
            while (on_time >= 0.1):
                src.append([num,n])
                on_time -= 0.1
                n+=1
            flag = False
        else:  # off周期
            off_time=random.expovariate(lambd2)#获得lambda=lambd2的指数分布off时间
            if (off_min> off_time):
                off_time=off_min
            #print(off_time)
            while (off_time >= 0.1):
                src.append(0)
                off_time -= 0.1
            flag = True
    return src
#流量生成
src1=generator(1,1.2,1.1)
src2=generator(2,1.5,1.2)
#print(src1)
#print(src2)
src=[]
f1 = open('test.txt','w')
#for i in range(100):
    #print(random.randint(0,1), end="")
if __name__ == '__main__':
    Simulation2.simulation2(src1,src2,f1).run(100,2)
    #f1.close()