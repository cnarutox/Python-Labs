import time
from threading import Thread, Semaphore
from random import randrange
from functools import reduce

I = 5
J = 4
N = 3
id = 0
vals = []

K1_lock = Semaphore(15)
K2_lock = Semaphore(15)


def ID():
    global id
    id += 1
    return id


class production():
    def __init__(self, id, producer, time, loc=0):
        self.id = id
        self.producer = producer
        self.time = time
        self.loc = loc


def produce_semaphone(empty, full, mutex, vals, i):
    while (True):
        if K1_lock.acquire(blocking=False) is False:
            print(f"生产者{i}拜拜")
            break
        # 生产
        t = time.asctime(time.localtime())
        p = production(ID(), i, t)
        print(f"{t}\t生产者 {i} 开始生产产品 {id}")
        time.sleep(randrange(1, 5))

        empty.acquire()
        print(f"{time.asctime(time.localtime())}\t生产者 {i} 试图进入公共缓冲区")
        mutex.acquire()
        print(f"{time.asctime(time.localtime())}\t生产者 {i} 进入了公共缓冲区！！")
        val = reduce(lambda x, y: x + y, [str(v.id) + ' '
                                          for v in vals] + [''])
        print(f"{time.asctime(time.localtime())}\t生产者 {i} 生产前的公共缓冲区\t{val}")

        p.loc = len(vals) + 1
        vals.append(p)
        val = reduce(lambda x, y: x + y, [str(v.id) + ' '
                                          for v in vals] + [''])
        print(f"{time.asctime(time.localtime())}\t生产者 {i} 生产后的公共缓冲区\t{val}")
        mutex.release()
        print(f"{time.asctime(time.localtime())}\t生产者 {i} 离开了公共缓冲区！！")
        full.release()


def consume_semaphone(empty, full, mutex, vals, i):
    while (True):
        if K2_lock.acquire(blocking=False) is False:
            print(f"消费者{i}拜拜")
            break

        full.acquire()
        print(f"{time.asctime(time.localtime())}\t消费者 {i} 试图进入公共缓冲区")
        mutex.acquire()
        print(f"{time.asctime(time.localtime())}\t消费者 {i} 进入了公共缓冲区！！")
        val = reduce(lambda x, y: x + y, [str(v.id) + ' '
                                          for v in vals] + ['', ''])
        print(f"{time.asctime(time.localtime())}\t消费者 {i} 消费前的公共缓冲区\t{val}")
        p = vals[-1]
        vals.pop(-1)
        val = reduce(lambda x, y: x + y, [str(v.id) + ' '
                                          for v in vals] + ['', ''])
        print(f"{time.asctime(time.localtime())}\t消费者 {i} 消费后的公共缓冲区\t{val}")
        mutex.release()
        print(f"{time.asctime(time.localtime())}\t消费者 {i} 离开了公共缓冲区！！")

        print(
            f"{time.asctime(time.localtime())}\t消费者 {i} 开始消费产品\t{p.id}\tid:{p.id}\tproducer:{p.producer}\tloc:{p.loc}"
        )
        time.sleep(randrange(1, 5))
        empty.release()


if __name__ == '__main__':

    # 使用信号量
    mutex = Semaphore(1)
    empty = Semaphore(N)
    full = Semaphore(0)
    pro = [
        Thread(
            target=produce_semaphone, args=(empty, full, mutex, vals, i + 1))
        for i in range(I)
    ]
    con = [
        Thread(
            target=consume_semaphone, args=(empty, full, mutex, vals, i + 1))
        for i in range(J)
    ]
    for p in pro:
        p.start()
    for c in con:
        c.start()
