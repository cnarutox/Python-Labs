import time
from threading import Thread, Lock, Semaphore, Condition
from queue import LifoQueue
from random import randrange
from functools import reduce

N = 10


def produce(queue, vals):
    while (True):
        p = chr(randrange(65, 97))
        queue.put(p)
        vals.append(p)
        val = reduce(lambda x, y: x + y, vals + [''])
        print(
            f"{time.asctime(time.localtime())}\t生产了 {p} 在 {queue.qsize()} 位置\t剩余空间 {N - queue.qsize()}\t{val}"
        )
        time.sleep(randrange(2.))


def consume(queue, vals):
    while (True):
        val = queue.get()
        p = vals[-1]
        vals.pop(-1)
        val = reduce(lambda x, y: x + y, vals + ['', ''])
        print(
            f'{time.asctime(time.localtime())}\t消费了 {p} 在 {queue.qsize() + 1} 位置\t剩余食物 {queue.qsize()}\t{val}'
        )
        time.sleep(randrange(2.))


def produce_semaphone(empty, full, mutex, vals):
    while (True):
        p = chr(randrange(65, 97))
        empty.acquire()
        mutex.acquire()
        vals.append(p)
        val = reduce(lambda x, y: x + y, vals + [''])
        mutex.release()
        full.release()
        print(
            f"{time.asctime(time.localtime())}\t生产了 {p} 在 {len(vals)} 位置\t剩余空间 {N - len(vals)}\t{val}"
        )
        time.sleep(randrange(2.))


def consume_semaphone(empty, full, mutex, vals):
    while (True):
        full.acquire()
        mutex.acquire()
        p = vals[-1]
        vals.pop(-1)
        val = reduce(lambda x, y: x + y, vals + ['', ''])
        mutex.release()
        empty.release()
        print(
            f'{time.asctime(time.localtime())}\t消费了 {p} 在 {len(vals) + 1} 位置\t剩余食物 {len(vals)}\t{val}'
        )
        time.sleep(randrange(2.))


def produce_cond(cond, vals):
    while (True):
        p = chr(randrange(65, 97))
        cond.acquire()
        while len(vals) == N:
            cond.wait()
        vals.append(p)
        val = reduce(lambda x, y: x + y, vals + [''])
        print(
            f"{time.asctime(time.localtime())}\t生产了 {p} 在 {len(vals)} 位置\t剩余空间 {N - len(vals)}\t{val}"
        )
        cond.notify()
        cond.release()
        time.sleep(randrange(2.))


def consume_cond(cond, vals):
    while (True):
        cond.acquire()  # 对内部锁上锁
        while len(vals) == 0:
            cond.wait()  # 使用wait前内部锁必须先上锁，wait之后内部锁自动释放，该线程等待被notify，被唤醒之后自动上锁
        p = vals[-1]
        vals.pop(-1)
        val = reduce(lambda x, y: x + y, vals + ['', ''])
        print(
            f'{time.asctime(time.localtime())}]\t消费了 {p} 在 {len(vals) + 1} 位置\t剩余食物 {len(vals)}\t{val}'
        )
        cond.notify()
        cond.release()
        time.sleep(randrange(2.))


if __name__ == '__main__':
    vals = []
    # 使用模块Queue，自动化地完美处理多线程问题
    q = LifoQueue(N)
    Thread(target=produce, args=(q, vals)).start()
    Thread(target=consume, args=(q, vals)).start()

    # 使用信号量
    mutex = Semaphore(1)
    empty = Semaphore(N)
    full = Semaphore(0)
    # Thread(target=produce_semaphone, args=(empty, full, mutex, vals)).start()
    # Thread(target=consume_semaphone, args=(empty, full, mutex, vals)).start()

    # 使用互斥量（参数为1的信号量也可作为互斥量）+条件变量
    lock = Lock()
    cond = Condition(lock)  # 条件变量必然会与一个锁关联（如果你不指定的话会自动关联一个RLock锁）
    # Thread(target=produce_cond, args=(cond, vals)).start()
    # Thread(target=consume_cond, args=(cond, vals)).start()
