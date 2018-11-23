import threading
# 读者优先
muter = threading.Semaphore(1)  # 锁readercount
wsem = threading.Semaphore(1)
rc = 0


def reader_prioritw():
    global rc
    while (True):
        muter.acquire()
        rc += 1
        if rc == 1:
            wsem.acquire()
        muter.release()
        # read_data_base()
        muter.acquire()
        rc -= 1
        if rc == 0:
            wsem.release()
        muter.release()
        # use_data_read()


def writer():
    while (True):
        # think_up_data()
        wsem.acquire()
        # write_data_base()
        wsem.release()


# 写者优先
rc = 0
wc = 0
r, w, z, wsem, rsem = [threading.Semaphore(1) for i in range(5)]


def reader():
    global rc
    while (True):
        z.acquire()  # z信号用来保证阻塞在rsem信号中排队的读者至多只有一个, 其余的阻塞在z上。
        rsem.acquire()
        r.acquire()
        rc += 1
        if (rc == 1):
            wsem.acquire()
        r.release()
        rsem.release()  # 写者抢占访问权的时机!
        z.release()

        # read()

        r.acquire()
        rc -= 1
        if (rc == 0):
            wsem.release()
        r.release()


def writer_priority():
    global wc
    while (True):
        w.acquire()
        wc += 1
        if (wc == 1):
            rsem.acquire()
        w.release()

        wsem.acquire()
        # write()
        wsem.release()

        w.acquire()
        wc -= 1
        if (wc == 0):
            rsem.release()
        w.release()
