import xlsxwriter
import datetime


def _readline(f):
    countList = f.readline().strip().split(' ')
    return countList

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
        'align': 'center',
    })
    baseFormat = payroll.add_format({
        'font_size': 14,
        'align': 'center',
    })
    ALLSALARY = {}  # NAME:SALARY

    with open('在这输入工资.txt', 'r', encoding='utf8') as f:
        # 读取带名字首行
        fileLinesNum = len(f.readlines())
        f.seek(0)
        dataList = _readline(f)
        curLine = 1

        while True:
            # if not dataList or not dataList[0]:
            #     print('读完了！（没读完的话检查是否有空行！！！）')
            #     break
            if curLine == fileLinesNum:
                break
            if not dataList or not dataList[0]:
                dataList = _readline(f)
                curLine += 1
                continue
            if dataList[0].isdigit():
                print('数据错误')
                break

            name, ratio = dataList
            totalSalary = 0
            day = 1
            workSheet = payroll.add_worksheet(name)
            workSheet.set_column('B:H', 15)  # 设置列宽
            headings = ['id', '计件', '计件', '计件', '计件', '计件', '日工', '工资(元)']

            while True:  # 日工资
                dataList = _readline(f)
                curLine += 1
                if dataList[0].isalpha() or not dataList[0]:  # 计算完一个人的工资，循环退出，打印总工资
                    print('------------------------------', name, ": ", "总工资：", totalSalary, '----------------------------------------------------')
                    print()

                    ALLSALARY[name] = totalSalary
                    workSheet.write_row('A2', headings, bold)
                    workSheet.merge_range('A1:H1', '%s 总工资：%s 元' % (name, totalSalary), bold)
                    break

                # 计算日工资
                daySalary, haveDayWork = _caculateDaySalary(dataList, ratio)
                totalSalary += daySalary
                print(day, ": ", daySalary)
                dataList.insert(0, day)
                dataList.append(daySalary)

                # 加空位
                blankNum = len(headings) - len(dataList)
                for _ in range(blankNum):
                    if haveDayWork:  # 有日工
                        dataList.insert(-2, '')
                    else:
                        dataList.insert(-1, '')
                workSheet.write_row('A%s' % (day+2), dataList, baseFormat)
                day += 1
            workSheet.write_formula('H%s' % (day+3), '=SUM(H3:H%s)' % (day+2), bold)

        # 写总表
        workSheet = payroll.add_worksheet('总表')
        workSheet.set_column('A:B', 15)
        HEAD = ['姓名', '本月工资']
        workSheet.write_row('A1', HEAD, bold)
        index = 1
        for i, name in enumerate(ALLSALARY):
            workSheet.write_row('A%s' % (index+1), [name, ALLSALARY[name]], baseFormat)
            index += 1

        workSheet.write('A%s' % (index+1), '总工资：', bold)
        workSheet.write_formula('B%s' % (index+1), '=SUM(B2:B%s)' % index, bold)

        payroll.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('-------------------错误开始-----------------------')
        print('内容：', e)

        # if e.text:
        #     print('提示: 有错误空格，行: %s' % e.text)

        print('-------------------错误结束-----------------------')

    input('输任意键关闭窗口，直接关也行！')



