import MySQLdb
import xlrd
import datetime

def opinet_value(cur_value, prev_value):
    value = 0.0

    if not cur_value or cur_value == '-':
        value = prev_value
    else:
        value = float(cur_value)

    return value;

MySQLdb.paramstyle = 'pyformat'

db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='visualization',charset='utf8',autocommit=True)

workbook = xlrd.open_workbook("./수출품목 중 상위 10개 품목 통계.xls")
worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows
ncols = worksheet.ncols

dataset = []

prev_dubai = prev_brent = prev_wti = 0.0;

for a in range(1, ncols, 2):
    for i in range(4, nrows-4):
        date = worksheet.cell_value(2, a)
        place = worksheet.cell_value(i, 0)
        name = worksheet.cell_value(i, a)
        value = worksheet.cell_value(i, a+1)

        dataset.append({
            'date': date,
            'place': place,
            'name': name,
            'value': int(value.replace(',',''))
        })

cur = db.cursor()

cur.executemany("""
    INSERT INTO export(date, place, name, value)
    VALUES (%(date)s, %(place)s, %(name)s, %(value)s)
    """, dataset)

db.commit()