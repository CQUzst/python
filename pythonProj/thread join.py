#使用join对控制多个线程的执行顺序非常关键
#t.join()方法只会使主线程进入等待池并等待t线程执行完毕后才会被唤醒
# 并不影响同一时刻处在运行状态的其他线程
import threading
import time
def thread_job():
    print('T1 start\n')
    for i in range(10):
        time.sleep(0.1)
    print('T1 finish\n')

def T2_job():
    print('T2 start\n')
    print('T2 finish\n')

def main():
    added_thread = threading.Thread(target=thread_job, name='T1')
    thread2 = threading.Thread(target=T2_job, name='T2')
    added_thread.start()
    thread2.start()
    thread2.join()
    added_thread.join()

    print('all done\n')

if __name__ == '__main__':
    main()
