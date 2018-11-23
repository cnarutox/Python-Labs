import time
import random
import threading

n = 5
thinking = 0
hungry = 1
eating = 2
state = [0 for i in range(n)]
mutex = threading.Semaphore(1)
s = [threading.Semaphore(1) for i in range(n)]
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
        forks_of_philosophers[2 * i + 1] = '🤮 '
        forks_of_philosophers[2 * i] = forks_of_philosophers[2 * i + 2] = ' '
        if 2 * i == 0:
            forks_of_philosophers[-1] = ' '
        elif i == n - 1:
            forks_of_philosophers[0] = ' '
        state[i] = eating
        s[i].release()


def think(i):
    rand = random.randrange(3, 10)
    print('philosopher {} is thinking 😴  for {}s {:<18} {}'.format(
        i + 1, rand, '⌛ ' * rand, ''.join(forks_of_philosophers)))
    time.sleep(rand)


def eat(i):
    rand = random.randrange(2, 7)
    print('philosopher {} is eating   🤮  for {}s {:<18} {}'.format(
        i + 1, rand, '⏳ ' * rand, ''.join(forks_of_philosophers)))
    time.sleep(rand)


def take_forks(i):
    mutex.acquire()
    state[i] = hungry
    test(i)
    mutex.release()
    s[i].acquire()


def put_forks(i):
    mutex.acquire()
    forks_of_philosophers[2 * i + 1] = '😴 '
    forks_of_philosophers[2 * i] = forks_of_philosophers[2 * i + 2] = '🍴'
    if 2 * i == 0:
        forks_of_philosophers[-1] = '🍴'
    elif i == n - 1:
        forks_of_philosophers[0] = '🍴'
    think(i)
    state[i] = thinking
    test(left(i))
    test(right(i))
    mutex.release()


def philosopher(i):
    think(i)
    while (True):
        if state[i] == thinking:
            take_forks(i)
        if state[i] == eating:
            eat(i)
            put_forks(i)


philosophers = [
    threading.Thread(target=philosopher, args=(i, )) for i in range(n)
]
if __name__ == '__main__':
    for i in philosophers:
        i.start()
