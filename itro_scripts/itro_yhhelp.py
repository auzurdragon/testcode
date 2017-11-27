import pandas
result = []
for i in range(1,10):
    data = pandas.read_excel('itro_scripts/11/6/06 (%d).xlsx' % i)
    tmp = data.get('收件人姓名 *')
    result = result +list(data.get('收件人姓名 *'))
    print('get %d logs' % len(tmp))

for i in range(1,12):
    data = pandas.read_excel('itro_scripts/11/7/07 (%d).xlsx' % i)
    tmp = data.get('收件人姓名 *')
    result = result + list(data.get('收件人姓名 *'))
    print('get %d logs' % len(tmp))

import xlrd
result2 = []
filepath = 'itro_scripts/11/8/08.xls'
file = xlrd.open_workbook(filepath)
sheetcount = len(file.sheets())
for i in file.sheets():
    print(i.name)
    data = pandas.read_excel(filepath,sheetname=i.name)
    tmp = data.get('收件人姓名 *')
    result2 = result2 + list(tmp)


