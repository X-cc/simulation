import random
import time
import queue
import threading

class simulation():
    def __init__(self,src1,src2,f1):
        self.src1=src1
        self.src2=src2
        self.f1=f1

    def run(self,dq_len,wq_num):
        drop=[]
        dqueue=queue.Queue(maxsize=dq_len)
        wqueue_list=[queue.Queue(maxsize=dq_len/wq_num) for i in range(wq_num)]
        threads=[]
        threads.append(threading.Thread(target=self.get_packet,args=[wqueue_list[0],self.src1,]))
        threads.append(threading.Thread(target=self.get_packet,args=[wqueue_list[1],self.src2,]))
        threads.append(threading.Thread(target=self.trans_packet,args=[wqueue_list,dqueue,]))
        threads.append(threading.Thread(target=self.deal_packet,args=[dqueue, ]))
        threads.append(threading.Thread(target=self.drop_packet,args=[wqueue_list,dqueue,]))
        threads.append(threading.Thread(target=self.print_qsize,args=[wqueue_list,dqueue,]))
        for thread in threads:
            thread.start()
        for t in threads:
            t.join(100)
    def get_packet(self,wqueue,src):
        for i in range(len(src)):
            if(src[i]!=0):
                wqueue.put(src[i])
                time.sleep(0.001)
                i+=1
            else:
                i+=1
                time.sleep(0.001)
    def trans_packet(self,wait_queue_list,deal_queue):
        while True:
            while(deal_queue.full()!=True):
                for i in range(len(wait_queue_list)):
                    print('loop to %s,len is%s'%((i+1),wait_queue_list[i].qsize()))
                    n=10
                    while (wait_queue_list[i].empty() != True)and(n!=0):
                        deal_queue.put(wait_queue_list[i].get())
                        time.sleep(0.001)
                        n-=1
                    time.sleep(0.01)  # 轮询1,2,切换时间0.01s
                    print('deal queue len is %s'%deal_queue.qsize())
                if(wait_queue_list[0].empty()==True)and(wait_queue_list[0].empty()==True):break


    def deal_packet(self, deal_queue):
        while True:
            while (deal_queue.empty() != True):
                #print('packet dealing...')
                deal_queue.get()
                #print(deal_queue.get())
                time.sleep(0.002)  # 每处理一个packet用时0.01s


    def drop_packet(self,wait_queue_list,deal_queue):
        while True:
            drop=[]
            for i in range(len(wait_queue_list)):
                #print('loop to %s,len is%s' % ((i + 1), wait_queue_list[i].qsize()))
                print('deal queue len is %s' % deal_queue.qsize())
                while(wait_queue_list[i].full()==True)and(deal_queue.full()==True):
                    print(time.time())
                    drop.append(wait_queue_list[i].get())
                    time.sleep(0.001)
            if(len(drop)!=0):
                self.f1.write('\n'+'drop happened!drop packet=%s,at %s'%(drop,time.clock()))
    def print_qsize(self,wait_queue_list,deal_queue):
        while True:
            self.f1.write('\n'+'When %s,wait queue 1 length is %s,wait queue 2 length is %s,deal queue length is %s'%(time.clock(),wait_queue_list[0].qsize(),wait_queue_list[1].qsize(),deal_queue.qsize()))
            time.sleep(0.001)