import time
import threading
from queue import Queue
from random import randrange


def produce(queue):
    while (not queue.full()):
        p = chr(randrange(65, 97))
        print('生产了', end='')
        queue.put(p)
        print(" {} 在 {} 位置\t剩余空间 {}\t{}".format(
            p, queue.qsize(), 50 - queue.qsize(),
            time.asctime(time.localtime(time.time()))))
        time.sleep(randrange(2.))


def consume(queue):
    while (not queue.full()):
        val = queue.get()
        print('消费了 {} 在 {} 位置\t剩余食物 {}\t{}'.format(
            val, queue.qsize() + 1, queue.qsize(),
            time.asctime(time.localtime(time.time()))))
        time.sleep(randrange(3.))


if __name__ == '__main__':
    funcs = [produce, consume]
    q = Queue(50)

    for i, f in enumerate(funcs):
        threading.Thread(target=f, args=(q, )).start()
