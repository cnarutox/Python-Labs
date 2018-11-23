import random
import threading
import time
'''
    The Sleeping-Barber Problem
    A barbershopconsists of a waiting room with n chairs and the barber room
    containing thebarber chair. If there are no customers to be served, the
    barber goes to sleep.If a customer enters the barbershop and all chairs are
    occupied, then thecustomer leaves the shop. If the barber is busy but
    chairs are available, thenthe customer sits in one of the free chairs. If
    the barber is asleep, thecustomer wakes up the barber. Write a program to
    coordinate the barber and the customers.
    🛌代表空座	😴代表等待	😁代表此时此刻轮到自己	🕺代表理发完成离开	🏌️‍代表无空座离开
    ┐
    |代表理发师的一个工作周期
    ┘
    本示例默认新来的顾客会在上一个等待的人的右边坐下，若上一个等待的人坐在最后一个座位，
    则考虑第一个座位；若没有等待的人，则坐在第一个座位
'''

chairs = 5
next_chair = 1  # 下一个（即将到来）顾客的座位
customers = threading.Semaphore(0)
barbers = threading.Semaphore(0)
mutex = threading.Semaphore(1)
waiting = 0
scene = ['🛌' for i in range(chairs)] + ['']


def barber():
    global waiting, next_chair, scene
    cus = 0
    while (True):
        customers.acquire()
        mutex.acquire()
        current_customer = ((next_chair + 5) - waiting - 1) % 5
        scene[current_customer] = '😁'
        waiting -= 1
        if waiting == 0:
            next_chair = 1
        print(f' Barber  cut  customer  {cus + 1:<5}\t', *scene[:-1], ' ┐')
        scene[-1] = ' |'
        # barbers.release()
        scene[current_customer] = '🛌'
        mutex.release()
        # 开始剪头发
        time.sleep(1 + random.random())
        scene[-1] = ''
        print(f' Barber  end  customer  {cus + 1:<5}\t', *scene[:-1], ' ┘',
              '🕺')
        barbers.release()
        cus += 1


def customer(cus):
    global waiting, next_chair, scene
    mutex.acquire()
    print(f'Customer {cus + 1:^3}', end=' ')
    if waiting < chairs:
        scene[next_chair - 1] = '😴'
        print(f'sits chair {next_chair}\t', *scene)
        waiting += 1
        next_chair = next_chair % 5 + 1
        customers.release()
        mutex.release()
        barbers.acquire()
        # get_haircut
    else:
        print(f'{"leave":^10}\t\t', *scene, '🏌️‍')
        mutex.release()


if __name__ == "__main__":
    cus = 0  # 顾客编号
    threading.Thread(target=barber).start()
    while True:
        threading.Thread(target=customer, args=(cus, )).start()
        time.sleep(0.5 + random.random())
        cus += 1
