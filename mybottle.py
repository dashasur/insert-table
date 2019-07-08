import psycopg2
from bottle import route, request, run

conn = psycopg2.connect(dbname='daria', user='daria', password='dasha50', host='192.168.4.12', port='5432', )
cursor = conn.cursor()


@route('/')
def a():
    postgres_select_query = """select id, "name" from "Public".currency"""
    cursor.execute(postgres_select_query)
    a = cursor.fetchall()
    b=""
    for i in a:
        b=b+"<option value=\""+str(i[0])+"\">" +i[1]+ "</option>\n"
    c=  '''<!DOCTYPE html>
<html>
<body>

        <form action="/c" method="post">
        <select name="id">'''+b+ '''</select>
        <select name="id">'''+b+ '''</select>
            <input value="отправить" type="submit" />
        </form></body>
</html>

'''
    return c


@route('/c', method='POST')
def c():
    c1 = request.forms.get('id')
    c2 = request.forms.get('id')

    return "<p>Got</p><br/>"+c1+"/ "+c2+"<br/>"
    

run(host='localhost', port=8080, debug=True)