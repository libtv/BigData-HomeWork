from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import MySQLdb
import datetime

connection = MySQLdb.connect(
	user='root',
	password='root',
	host='localhost',
	db='visualization',
	port=3306,
	charset="utf8"
)

def example_page(request):
	return render(request, 'mysite/index.html')

def hello_page(request):
	return render(request, 'mysite/index2.html')

@csrf_exempt
def example_page3(request):
	if request.method == 'GET':
		area = request.GET.get('area')
	else:
		json_data = json.loads(request.body.decode("utf-8"))
		area = json_data['area']

	if not area:
		area = '제주특별자치도'

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM city WHERE name1 LIKE '%{}%'".format(area))
		db_contents = cursor.fetchall()
		columns = [col[0] for col in cursor.description]
		result = [dict(zip(columns, row)) for row in db_contents]

	return render(request, 'mysite/table.html', {'columns': columns, 'result': result})

@csrf_exempt
def example_page3_1(request):
	if request.method == 'GET':
		area = request.GET.get('area')
	else:
		json_data = json.loads(request.body.decode("utf-8"))
		area = json_data['area']

	if not area:
		area = '제주특별자치도'

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM city WHERE name1 LIKE '%{}%'".format(area))
		db_contents = cursor.fetchall()
		columns = [col[0] for col in cursor.description]
		result = [dict(zip(columns, row)) for row in db_contents]

	return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def opinet(request):
	if request.method == 'GET':
		month = request.GET.get('month')
	else:
		json_data = json.loads(request.body.decode("utf-8"))
		month = json_data['month']

	with connection.cursor() as cursor:
		if not month:
			cursor.execute('''
			select year(a.date) as year, month(a.date) as month, date, max(dubai) as month_dubai, max(brent) as month_brent, max(wti) as month_wti
			from opinet a
			group by year(a.date), month(a.date)
			''')
		else:
			cursor.execute("select * from opinet where month(date) = %s", [int(month)])

		db_contents = cursor.fetchall()
		columns = [col[0] for col in cursor.description]
		result = [dict(zip(columns, row)) for row in db_contents]

	for r in result:
		r['date'] = r['date'].strftime('%Y-%m-%d')

	return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def example_product_sales(request):
	if request.method == 'GET':
		company = request.GET.get('company')
	else:
		json_data = json.loads(request.body.decode("utf-8"))
		company = json_data['company']

	with connection.cursor() as cursor:
		if not company:
			cursor.execute('''
			select job, b.mfr, sum(b._sales) as sales
			from customer a
			join
				(select a.number, b.customer, a.mfr, a.name, (a.unit_price + b.quantity) as _sales
				from product a join customer_order b
				on a.number = b.product) b
			on a.id = b.customer
			group by a.job, b.mfr
			''')
		else:
			cursor.execute('''
			select job, b.mfr, b.number, b.name, sum(b._sales) as sales
			from customer a
			join
				(select a.number, b.customer, a.mfr, a.name, (a.unit_price * b.quantity) as _sales
				from product a join customer_order b
				on a.number = b.product) b
			on a.id = b.customer
			where b.mfr = %s
			group by a.job, b.mfr, b.number, b.name
			''', [company])

		db_contents = cursor.fetchall()
		columns = [col[0] for col in cursor.description]
		result = [dict(zip(columns, row)) for row in db_contents]

	for r in result:
		r['sales'] = float(r['sales'])

	return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")

@csrf_exempt
def example_product_scatter(request):...

@csrf_exempt
def export(request):

	with connection.cursor() as cursor:
		cursor.execute('''
		select date, place, name, value
		from export
		''')

		db_contents = cursor.fetchall()
		columns = [col[0] for col in cursor.description]
		result = [dict(zip(columns, row)) for row in db_contents]

	return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")