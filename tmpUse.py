import xlsxwriter
import datetime


def _readline(f):
    myList = f.readline().strip().split(' ')
    return myList

def _caculateDaySalary(countList, ratio):
    daySalary = 0
    haveDayWork = False
    for i in countList:
        if '*' in i:
            daySalary += eval(i)
        else:
            daySalary += float(i) * float(ratio)
            haveDayWork = True
    return round(daySalary, 1), haveDayWork

def main():
    dt = datetime.datetime.now()
    payroll = xlsxwriter.Workbook('%s-%s-%s工资表.xlsx' % (dt.year, dt.month, dt.day))
    bold = payroll.add_format({
        'bold': True,
        'font_size': 15,
    })
    baseFormat = payroll.add_format({
        'font_size': 14,
    })

    with open('月工资输入.txt', 'r', encoding='utf8') as f:
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
            workSheet = payroll.add_worksheet(name)
            workSheet.set_column('B:H', 15)
            headings = ['id', '计件', '计件', '计件', '计件', '计件', '日工', '当日工资']

            while True:  # 日工资
                dataList = _readline(f)
                if dataList[0].isalpha() or not dataList[0]:
                    print('------------------------------', name, ": ", "总工资：", totalSalary, '----------------------------------------------------')
                    print()
                    workSheet.write_row('A1', headings, bold)
                    workSheet.write_row('A%s' % (day+1), ['', '', '', '', '', '', '总工资:', totalSalary], bold)
                    break
                daySalary, haveDayWork = _caculateDaySalary(dataList, ratio)
                totalSalary += daySalary
                print(day, ": ", daySalary)
                dataList.insert(0, day)
                dataList.append(daySalary)
                extraNum = len(headings) - len(dataList)
                for _ in range(extraNum):
                    if haveDayWork:
                        dataList.insert(-2, '')
                    else:
                        dataList.insert(-1, '')
                workSheet.write_row('A%s' % (day+1), dataList, baseFormat)
                day += 1

        payroll.close()


if __name__ == '__main__':
    main()
    # input('输任意键关闭窗口，直接关也行！')



