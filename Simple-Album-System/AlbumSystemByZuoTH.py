import os
import time


def length(mystr: str):
    result = 0
    for i in mystr:
        if ord(i) < 128:
            result += 1
        else:
            result += 2
    return result


def center(mystr: str, mylength):
    mywhitelen = (mylength - length(mystr)) // 2
    result = ' ' * mywhitelen + mystr + ' ' * mywhitelen
    return result if mywhitelen * 2 + length(
        mystr) == mylength else result + ' '


class PhoneBook:
    EVERY_LINE = 60

    def __init__(self):
        self._operations = {
            'i': self._insert,
            'I': self._insert,
            's': self._select,
            'S': self._select,
            'd': self._delete,
            'D': self._delete,
            'u': self._update,
            'U': self._update,
            'q': exit,
            'Q': exit
        }
        self._database = {}

    def _clear_screen(self):
        os.system('cls')

    def _print_header(self):
        self._adjust_print('序号', self.EVERY_LINE // 5, '')
        self._adjust_print('学号', self.EVERY_LINE // 5, '')
        self._adjust_print('姓名', self.EVERY_LINE // 5, '')
        self._adjust_print('电话', self.EVERY_LINE // 5, '')
        self._adjust_print('邮箱', self.EVERY_LINE // 5)

    def _print_person(self, person_number):
        self._adjust_print(self._database[person_number][0],
                           self.EVERY_LINE // 5, '')
        self._adjust_print(person_number, self.EVERY_LINE // 5, '')
        self._adjust_print(self._database[person_number][1],
                           self.EVERY_LINE // 5, '')
        self._adjust_print(self._database[person_number][2],
                           self.EVERY_LINE // 5, '')
        self._adjust_print(self._database[person_number][3],
                           self.EVERY_LINE // 5)

    def _insert(self):
        self._clear_screen()
        this_data = []
        print('请输入您的学号：')
        this_number = input()
        if this_number in self._database:
            self._print_message('学号重复，请检查输入！')
            return
        this_data.append(str(len(self._database) + 1))
        print('请输入您的姓名：')
        this_data.append(input())
        print('请输入您的电话：')
        this_data.append(input())
        print('请输入您的邮箱：')
        this_data.append(input())
        self._database[this_number] = this_data
        self._print_message('添加成功！')

    def _select(self):
        self._clear_screen()
        print('*' * self.EVERY_LINE)
        self._print_header()
        for i in self._database:
            self._print_person(i)
        print('*' * self.EVERY_LINE)
        print('按下回车键返回...')
        input()

    def _delete(self):
        self._clear_screen()
        print('请输入您想删除的人的学号：')
        this_number = input()
        if this_number not in self._database:
            self._print_message('学号不存在，请检查输入！')
            return
        print('您要删除的人的信息如下：')
        print()
        self._print_header()
        self._print_person(this_number)
        print()
        print('删除后无法恢复，确认删除请输入y')
        if input() == 'y':
            del self._database[this_number]
            self._print_message('删除成功')
        else:
            self._print_message('您取消了操作')

    def _update(self):
        self._clear_screen()
        this_data = []
        print('请输入您想修改的人的学号：')
        this_number = input()
        if this_number not in self._database:
            self._print_message('学号不存在，请检查输入！')
            return
        print('您要修改的人的信息如下：')
        print()
        self._print_header()
        self._print_person(this_number)
        print()
        this_data.append(self._database[this_number][0])
        print('请输入新的姓名：')
        this_data.append(input())
        print('请输入新的电话：')
        this_data.append(input())
        print('请输入新的邮箱：')
        this_data.append(input())
        self._database[this_number] = this_data
        self._print_message('修改成功！')

    def _print_menu(self):
        self._clear_screen()
        print('*' * self.EVERY_LINE)
        self._adjust_print('欢迎使用通讯录系统')
        self._adjust_print('添加数据请按[i]')
        self._adjust_print('查看数据请按[s]')
        self._adjust_print('删除数据请按[d]')
        self._adjust_print('修改数据请按[u]')
        self._adjust_print('退出系统请按[q]')
        print('*' * self.EVERY_LINE)
        self._adjust_print('请输入您要进行的操作：')

    def _print_message(self, message):
        print(message)
        time.sleep(1)

    def _adjust_print(self, mystr, mylength=EVERY_LINE, myend='\n'):
        print_result = ''
        if length(mystr) <= mylength:
            print_result = mystr
        else:
            for i in mystr:
                if length(print_result + i) > mylength - 3:
                    break
                print_result += i
            print_result += '...'
        print(center(print_result, mylength), end=myend)

    def messageloop(self):
        while True:
            self._print_menu()
            this_input = input()
            try:
                self._operations[this_input]()
            except KeyError:
                self._print_message('输入有误，请检查！')


if __name__ == '__main__':
    PhoneBook().messageloop()
