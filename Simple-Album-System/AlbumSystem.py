import re
'''未加正则匹配判断输入格式，但实现了表格自动加宽与中英混输'''


def len_whole_angle(char):
    '''判断是否为全角'''
    return sum([1 for c in char if not (0x20 <= ord(c) < 0x7e)])
    # 空格比较特殊，全角为 12288（0x3000），半角为 32（0x20）


def Len(str):
    return len(str) + len_whole_angle(str)


class Album:
    ''''''

    def __init__(self, width, albums, info, info_len, judge):
        self.judge = judge
        self.print_main(width)
        while True:
            command = input('>>>请输入命令对应的字母（按q返回菜单）：').lower()
            if command in ['a', 's', 'd', 'm', 'q']:
                if command == 'a':
                    self.append_datum(albums, info, info_len)
                elif command == 's':
                    self.display_data(albums, info, info_len)
                elif command == 'd':
                    self.delete_datum(albums, info, info_len)
                elif command == 'm':
                    self.modify_datum(albums, info, info_len)
                else:
                    self.print_main(width)
                    continue
            else:
                print('您输入的命令不存在，请重新输入！')

    def print_main(self, width):
        '''打印主菜单'''
        print('#' * width)
        print(
            '南开大学软件学院通讯录管理系统'.center(width -
                                     len_whole_angle('南开大学软件学院通讯录管理系统')), '\n')
        print('添加数据请按[a]'.center(width - len_whole_angle('添加数据请按[a]')))
        print('查看数据请按[s]'.center(width - len_whole_angle('查看数据请按[s]')))
        print('删除数据请按[d]'.center(width - len_whole_angle('删除数据请按[d]')))
        print('修改数据请按[m]'.center(width - len_whole_angle('修改数据请按[m]')), '\n')
        print('返回菜单请按[q]'.rjust(width - len_whole_angle('返回菜单请按[q]')))
        print('#' * width, '\n')

    def print_table_title(self, albums, info, info_len):
        '''打印表头'''
        for i, v in enumerate(info[1:]):
            length = Len(max(albums, key=lambda x: Len(x[v]))[v])
            if info_len[i + 1] < length:
                info_len[i + 1] = length
        print('{{:-^{}}}-{{:-^{}}}-{{:-^{}}}-{{:-^{}}}-{{:-^{}}}--'.format(
            *info_len).format(*['' for i in range(5)]))
        print('|{{:^{}}}|{{:^{}}}|{{:^{}}}|{{:^{}}}|{{:^{}}}|'.format(
            *[v - len_whole_angle(info[i])
              for i, v in enumerate(info_len)]).format(*info))
        print('|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|'.format(
            *info_len).format(*['' for i in range(5)]))

    def append_datum(self, albums, info, info_len):
        datum = {}.fromkeys(info[1:])
        for i, s in enumerate(info[1:]):
            datum[s] = input('>>>请输入您的{}：'.format(s)).strip()
            while not self.judge[i](datum[s]):
                datum[s] = input('>>>{}不正确，请重新输入：'.format(s)).strip()
        albums.append(datum)
        self.print_table_title(albums, info, info_len)
        print('|{{:^{}}}|{{:^{}}}|{{:^{}}}|{{:^{}}}|{{:^{}}}|'.format(
            info_len[0], *[
                v - len_whole_angle(list(datum.values())[i])
                for i, v in enumerate(info_len[1:])
            ]).format(len(albums), *datum.values()))
        print('|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|'.format(
            *info_len).format(*['' for i in range(5)]))

    def display_data(self, albums, info, info_len):
        if albums == []:
            print('无可显示数据！')
            return
        self.print_table_title(albums, info, info_len)
        for i, datum in enumerate(albums):
            print('|{{:^{}}}|{{:^{}}}|{{:^{}}}|{{:^{}}}|{{:^{}}}|'.format(
                info_len[0], *[
                    v - len_whole_angle(list(datum.values())[i])
                    for i, v in enumerate(info_len[1:])
                ]).format(i + 1, *datum.values()))
            print('|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|{{:-^{}}}|'.format(
                *info_len).format(*['' for i in range(5)]))

    def delete_datum(self, albums, info, info_len):
        if albums == []:
            print('无可删除数据！')
            return
        self.display_data(albums, info, info_len)
        try:
            index = int(input('>>>请输入要删除的数据序号：').strip())
            if index - 1 < 0 or index > len(albums):
                raise IndexError
            del albums[index - 1]
        except (IndexError, ValueError):
            print('您输入的序号不正确！')
        else:
            print('删除成功')

    def modify_datum(self, albums, info, info_len):
        if albums == []:
            print('无可修改数据！')
            return
        self.display_data(albums, info, info_len)
        try:
            index = int(input('>>>请输入要修改的数据序号：').strip())
            if index - 1 < 0 or index > len(albums):
                raise IndexError
            for i, s in enumerate(info[1:]):
                inp = input('>>>请输入您新的{}：'.format(s))
                while not self.judge[i](inp):
                    inp = input('>>>{}不正确，请重新输入：'.format(s)).strip()
                if inp:
                    albums[index - 1][s] = inp.strip()
        except (IndexError, ValueError):
            print('您输入的序号不正确！')
        else:
            print('修改成功')


if __name__ == '__main__':
    width = 60
    albums = []
    info = ['序号', '姓名', 'QQ', '电话', '邮箱']
    info_len = [6, 12, 12, 12, 20]
    judge = [
        lambda n: True,
        lambda q: q.isdigit(),
        lambda p: True if re.match('((\d+-)?\d+)', p) and re.match(
            '((\d+-)?\d+)', p).groups()[0] == p else False,
        lambda m: True if re.match(
            '([\w-]+@(\w+)+(\.[\w]+)+)', m) and re.match(
                '([\w-]+@(\w+)+(\.[\w]+)+)', m).groups()[0] == m else False
    ]
    Album(width, albums, info, info_len, judge)
