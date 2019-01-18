import threading
# 读者优先
rc = threading.Semaphore(1)  # 锁readercount
wsem = threading.Semaphore(1)
reader_count = 0


def reader_priority():
    global reader_count
    while (True):
        rc.acquire()
        reader_count += 1
        if reader_count == 1:
            wsem.acquire()
        rc.release()
        # read_data_base()
        rc.acquire()
        reader_count -= 1
        if reader_count == 0:
            wsem.release()
        rc.release()


def writer():
    while (True):
        # think_up_data()
        wsem.acquire()
        # write_data_base()
        wsem.release()


# 读写公平
rc = threading.Semaphore(1)  # 锁readercount
wsem = threading.Semaphore(1)
queue = threading.Semaphore(1)  # 公平竞争的队列锁
reader_count = 0


def reader_balance():
    global reader_count
    while (True):
        queue.acquire()
        rc.acquire()
        reader_count += 1
        if reader_count == 1:
            wsem.acquire()
        rc.release()
        queue.release()
        # read_data_base()
        rc.acquire()
        reader_count -= 1
        if reader_count == 0:
            wsem.release()
        rc.release()


def writer_balance():
    while (True):
        # think_up_data()
        queue.acquire()
        wsem.acquire()
        queue.release()
        # write_data_base()
        wsem.release()


# 写者优先
reader_count = 0
write_count = 0
rc, wc, z, wsem, rsem = [threading.Semaphore(1) for i in range(5)]
'''
z是否必须呢？假设没有z，想象一读者更新readercount、一读者和一写者阻塞的时序：rc此时被锁，
意味着有一读者运行在line 88 - line 91之间，在line 85还有一读者被阻塞， 
line 112也有一写者被阻塞，当读者更新完readercount，执行完resm.release()后，
阻塞中的读者和写者都有可能被唤醒，达不到写者优先的效果
'''


def reader():
    global reader_count
    while (True):
        z.acquire()  # z信号用来保证阻塞在rsem信号中排队的读者至多只有一个, 其余的阻塞在z上。
        rsem.acquire()

        rc.acquire()
        reader_count += 1
        if (reader_count == 1):
            wsem.acquire()
        rc.release()

        rsem.release()  # 写者抢占访问权的时机!
        z.release()

        # read_data_base()

        rc.acquire()
        reader_count -= 1
        if (reader_count == 0):
            wsem.release()
        rc.release()


def writer_priority():
    global write_count
    while (True):
        # think_up_data()
        wc.acquire()
        write_count += 1
        if (write_count == 1):
            rsem.acquire()
        wc.release()

        wsem.acquire()
        # write_data_base()
        wsem.release()

        wc.acquire()
        write_count -= 1
        if (write_count == 0):
            rsem.release()
        wc.release()


if __name__ == "__main__":
    threading.Thread(target=reader).start()
    threading.Thread(target=writer_priority).start()