import psycopg2
import ccxt

try:
    conn = psycopg2.connect(dbname='daria', user='daria', password='dasha50', host='192.168.4.12', port='5432', )
    cursor = conn.cursor()
     
    postgres_select_query = """Select id,name from "Public".currency"""
    cursor.execute(postgres_select_query)
    a = cursor.fetchall()
    d = {}
    for i in a:
        d[i[1]]=i[0]
    #print(d)
    #print(d['BTC'])
    g = ccxt.poloniex().load_markets()

    for i in g:
        a= i.split('/')
        # print (a)
        #print ("a ",a[0],a[1])
        #print ("d ",d[a[0]],d[a[1]])
        b=d[a[0]]
        q=d[a[1]]
        print(b,q)
    
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


    


