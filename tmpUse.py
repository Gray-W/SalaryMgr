



def _readline(f):
    myList = f.readline().strip().split(' ')
    return myList

def _caculateDaySalary(countList, ratio):
    daySalary = 0
    for i in countList:
        if '*' in i:
            daySalary += eval(i)
        else:
            daySalary += float(i) * float(ratio)
    return round(daySalary, 1)

def main():
    with open('monthOutput.txt', 'r', encoding='utf8') as f:
        dataList = _readline(f)
        while True:
            if not dataList or not dataList[0]:
                print('读完了！（没读完的话检查是否有空行！！！）')
                break
            if dataList[0].isdigit():
                print('数据错误')
                break

            name, ratio = dataList
            totalSalary = 0
            day = 1
            print('------------------------------', name, '工资表----------------------------------------------')

            while True:  # 日工资
                dataList = _readline(f)
                if dataList[0].isalpha() or not dataList[0]:
                    print('------------------------------', name, ": ", "总工资：", totalSalary, '----------------------------------------------------')
                    print()
                    break
                daySalary = 0
                daySalary = _caculateDaySalary(dataList, ratio)
                totalSalary += daySalary
                print(day, ": ", daySalary)
                day += 1


if __name__ == '__main__':
    main()
    input('点击任意键退出！')


