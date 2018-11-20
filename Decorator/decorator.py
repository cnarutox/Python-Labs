logs = []


def log(level, name=None, message=None):
    def decorate(func):
        def wrapper(*args, **kwargs):
            log = dict.fromkeys(['level', 'name', 'msg'])
            log['level'] = level
            log['name'] = name if name else func.__name__
            log['msg'] = message if message else func.__module__
            logs.append(log)
            return func(*args, **kwargs)

        return wrapper

    return decorate


@log(0, message='add x and y')
def add(x, y):
    return x + y


@log(1, 'output')
def output(*str):
    print(*str)


print(add(1, 2))
output(1, 2, 3)
print(logs)
