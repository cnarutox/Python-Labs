import time
import random
import threading

n = 5
thinking = 0
hungry = 1
eating = 2
state = [0 for i in range(n)]
mutex = threading.Semaphore(1)
print_lock = threading.Semaphore(1)  # 用来控制输出的锁
s = [threading.Semaphore(0) for i in range(n)]
philosophers = []
forks_of_philosophers = [
    '🍴', '😴 ', '🍴', '😴 ', '🍴', '😴 ', '🍴', '😴 ', '🍴', '😴 ', '🍴'
]


def left(i):
    return (i + n - 1) % n


def right(i):
    return (i + 1) % n


def test(i):
    if (state[i] == hungry and state[left(i)] != eating
            and state[right(i)] != eating):

        # 输出
        print_lock.acquire()
        forks_of_philosophers[2 * i + 1] = '🤮 '
        forks_of_philosophers[2 * i] = forks_of_philosophers[2 * i + 2] = ' '
        if 2 * i == 0:
            forks_of_philosophers[-1] = ' '
        elif i == n - 1:
            forks_of_philosophers[0] = ' '
        print_lock.release()
        # #

        state[i] = eating
        s[i].release()


def think(rand):
    time.sleep(rand)


def eat(i):
    rand = random.randrange(2, 7)

    # 输出
    print_lock.acquire()
    print('philosopher {} is eating   🤮  for {}s {:<18} {}'.format(
        i + 1, rand, '⏳ ' * rand, ''.join(forks_of_philosophers)))
    print_lock.release()
    # #

    time.sleep(rand)


def take_forks(i):
    mutex.acquire()
    state[i] = hungry
    test(i)
    mutex.release()
    s[i].acquire()


def put_forks(i):
    mutex.acquire()
    rand = random.randrange(3, 10)

    # 输出
    print_lock.acquire()
    forks_of_philosophers[2 * i + 1] = '😴 '
    forks_of_philosophers[2 * i] = forks_of_philosophers[2 * i + 2] = '🍴'
    if 2 * i == 0:
        forks_of_philosophers[-1] = '🍴'
    elif i == n - 1:
        forks_of_philosophers[0] = '🍴'
    # start thinking
    print('philosopher {} is thinking 😴  for {}s {:<18} {}'.format(
        i + 1, rand, '⌛ ' * rand, ''.join(forks_of_philosophers)))
    print_lock.release()
    # #

    state[i] = thinking
    test(left(i))
    test(right(i))
    mutex.release()
    return rand


def philosopher(i):
    while (True):
        take_forks(i)
        eat(i)
        think(put_forks(i))


philosophers = [
    threading.Thread(target=philosopher, args=(i, )) for i in range(n)
]
if __name__ == '__main__':
    for i in philosophers:
        i.start()
