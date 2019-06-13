import psycopg2

try:
    conn = psycopg2.connect(dbname='daria', user='daria', password='dasha50', host='192.168.4.12', port='5432', )
    cursor = conn.cursor()
     
    postgres_select_query = """Select id,name from "Public".currency"""
    cursor.execute(postgres_select_query)
    a = cursor.fetchall()
    d = {}
    for i in a:
        d[i[1]]=i[0]
    print(d)
    print(d['BTC'])
    conn.commit()
    
except (Exception, psycopg2.Error) as error :
    if(conn):
        print("Failed", error)
finally:
    #closing database connection.
    if(conn):
        if (cursor):
            cursor.close()
        conn.close()
    print("PostgreSQL connection is closed")
