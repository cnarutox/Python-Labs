class Lottery:
    def __init__(self, win=([], []), ranges=(range(0), range(0)), count=(0,
                                                                         0)):
        self.win = win
        self.ranges = ranges
        self.count = count

    def checkFormat(self, num):
        if len(set(num[0])) != self.count[0] or len(set(
                num[1])) != self.count[1]:
            raise ValueError
        for i, n in enumerate(num):
            for nn in n:
                if nn not in self.ranges[i]:
                    raise ValueError

    def get_same(self, num):
        return len([
            i for i in num[:self.count[1]][0]
            if i in self.win[:self.count[0]][0]
        ])

    def start(self, num):
        return self.get_level(num)


class DoubleLottery(Lottery):
    def __init__(self, type):
        super().__init__(*type)
        self.rule = {
            '一': [(6, 1)],
            '二': [(6, 0)],
            '三': [(5, 1)],
            '四': [(5, 0), (4, 1)],
            '五': [(4, 0), (3, 1)],
            '六': [(2, 1), (1, 1), (0, 1)]
        }

    def get_level(self, num):
        self.checkFormat(num)
        bef = self.get_same(num)
        aft = 1 if num[1] == self.win[1] else 0
        for k, v in self.rule.items():
            if (bef, aft) in v:
                return k
        return 0


class HappyLottery(Lottery):
    def __init__(self, type):
        super().__init__(*type)
        self.rule = {
            '一': [(5, 2)],
            '二': [(5, 1)],
            '三': [(5, 0), (4, 2)],
            '四': [(4, 1), (3, 2)],
            '五': [(4, 0), (3, 1), (2, 2)],
            '六': [(3, 0), (1, 2), (2, 1), (0, 2)]
        }

    def get_level(self, num):
        self.checkFormat(num)
        bef = self.get_same(num)
        aft = len([i for i in num[1] if i in self.win[1]])
        for k, v in self.rule.items():
            if (bef, aft) in v:
                return k
        return 0


try:
    if __name__ == '__main__':
        num = ([], [])
        types = [{
            'class': DoubleLottery,
            'win': ([3, 7, 9, 22, 27, 33], [12]),
            'ranges': (range(1, 34), range(1, 17)),
            'count': (6, 1)
        },
                 {
                     'class': HappyLottery,
                     'win': ([18, 14, 27, 8, 35], [9, 2]),
                     'ranges': (range(1, 36), range(1, 12)),
                     'count': (5, 2)
                 }]
        index = int(input('请选择玩法 输入数字：1.双色球，2.大乐透：')) - 1
        print('请输入前{}个中奖号码，范围为{}-{}'.format(types[index]['count'][0],
                                            types[index]['ranges'][0][0],
                                            types[index]['ranges'][0][-1]))
        for i in range(types[index]['count'][0]):
            num[0].append(int(input()))
        print('请输入后{}个中奖号码，范围为{}-{}'.format(types[index]['count'][1],
                                            types[index]['ranges'][1][0],
                                            types[index]['ranges'][1][-1]))
        for i in range(types[index]['count'][1]):
            num[1].append(int(input()))
        level = types[index]['class'](list(
            types[index].values())[1:]).start(num)
        print('中奖号码是{}{}'.format(*types[index]['win']))
        if level != 0:
            print('您中{}等奖'.format(level))
        else:
            print('您没有中奖')
            print(num)
except Exception:
    print('您的输入格式错误')
