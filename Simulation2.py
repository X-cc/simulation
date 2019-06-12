import queue
import time
import random

class simulation2:
    def __init__(self,src1,src2,f1):
        self.src1=src1
        self.src2=src2
        self.f1=f1
        self.time=0
        self.n1=0
        self.n2=0
        #self.flaglist=[True,False]
    def run(self,dq_len,wq_num):
        flaglist=[True,False]
        dqueue=queue.Queue(maxsize=dq_len)
        wqueue_list=[queue.Queue(maxsize=dq_len/wq_num) for i in range(wq_num)]
        wqueue_flag=[False,False]
        n=0
        deal_flag=False
        while True:
            self.get_packet(self.src1,n,wqueue_list[0],wqueue_flag[0])
            self.get_packet(self.src2,n,wqueue_list[1],wqueue_flag[1])
            n=n+1
            self.time=0.1*n
            flaglist,deal_flag=self.loop_queue(wqueue_list,wqueue_flag,flaglist,dqueue,deal_flag)
            deal_time=random.randint(0,1)
            if(deal_time==0)and(deal_flag==False):
                print('deal packet')
                self.deal_packet(dqueue)
            print(flaglist)
            time.sleep(0.2)
            print('When %s,len1=%s,len2=%s,deal queue=%s'%(self.time,wqueue_list[0].qsize(),wqueue_list[1].qsize(),dqueue.qsize()))

    def get_packet(self,src,n,wait_queue,wait_flag):
        if (src[n]==0):
            n+=1
        else:
            if(wait_queue.full()==True):
                self.drop_packet(wait_queue)
            if(wait_queue.empty()==True):
                wait_flag=True#表示刚存入，不可在本次循环处理
            else:
                wait_flag=False
            wait_queue.put(src[n])
            n+=1
            #print(wait_flag)
        return n,wait_flag

    def loop_queue(self,wait_queue_list,wait_flag,flag_list,deal_queue,deal_flag):
        for i in range(len(wait_queue_list)):
            if(flag_list[i]==True):
                print('should get from wait queue %s'%i)
                #判断轮询哪一队列
                if(wait_queue_list[i].empty()==True)or(wait_flag[i]==True):#如果缓存队列空或不可执行本次循环则轮询下一队列,flag不改变
                    print('wait queue %s is empty,turn to %s'%(i,i+1))
                    if(i!=len(wait_queue_list)-1):
                        i=i+1
                    else:
                        i=0
                elif(wait_queue_list[i].empty()==False)and(wait_flag[i]==False):#如果缓存队列不空，且可执行本次循环，修改flag，为下次轮询做准备
                    flag_list[i]=False
                    if (i != len(wait_queue_list) - 1):
                        flag_list[i+1]=True
                    else:
                        flag_list[0] = True
                #传输
                if (deal_queue.full()!=True)and(wait_queue_list[i].empty()!=True):#如果处理队列不满则存入
                    print('get from wait queue %s' % i)
                    if(wait_flag[i]==False):
                        if(deal_queue.empty()==True):
                            deal_flag=True#刚存入不能在此次循环处理
                        else:
                            deal_flag=False
                            break
                        deal_queue.put(wait_queue_list[i].get())
                    else:break
                    print('deal_flag=%s' %deal_flag)
                elif(deal_queue.full()==True)and(wait_queue_list[i].full()==True):#都满则抛出
                    self.drop_packet(wait_queue_list[i])
                    break
                elif(wait_queue_list[i].empty()==True):break#处理队列空或不能在此循环处理
            elif(flag_list[i]==False)and(wait_queue_list[i].empty()!=True):
                if(wait_queue_list[i].full()==True):
                    self.drop_packet(wait_queue_list[i])
                    break
                if(wait_queue_list[i].empty()==True):break
        return flag_list,deal_flag

    def deal_packet(self,deal_queue):
        if(deal_queue.empty()!=True):
            print(deal_queue.get())

    def drop_packet(self,wait_queue):
        drop=wait_queue.get()
        print('!!!!!!!!!!!!!!drop happened %s'%drop)

