import os
import re
import getpass
import socket


def cd(com):
    os.chdir(com[1])


def exit(com):
    raise KeyboardInterrupt


def exec(builtin, command):
    try:
        if command[0] in builtin.keys():
            builtin[command[0]](command)
        else:
            pid = os.fork()
            if pid == 0:
                os.execvp(command[0], command)
            elif pid > 0:
                os.waitpid(pid, 0)
                print('I am parent process pid' + str(os.getpid()))
    except KeyboardInterrupt:
        print('Exit!')
        return 0
    except FileNotFoundError:
        print('No such command!')
        return 0
    except IndexError:
        print('Args lack!')
    except Exception:
        print('Error')
        return 0
    return 1


def loop():
    state = 1
    builtin = {'cd': cd, 'exit': exit}
    while state:
        print(
            '{}@{}:~{}$'.format(getpass.getuser(), socket.gethostname(),
                                os.getcwd()),
            end=' ')
        command = re.split('\s', input())
        state = exec(builtin, command)


loop()
