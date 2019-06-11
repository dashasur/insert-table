import ccxt
import pprint
import psycopg2

def f1(cursor,curr) :
    postgres_select_query1 = """ SELECT count(*) cnt FROM "Public".currency WHERE "name"= %s """# check record
    record_to_insert = (curr,)
    cursor.execute(postgres_select_query1,record_to_insert)
    #print("f1 exec")
    c = cursor.fetchall()
    #print("f1 fetch",c)
    b = c[0][0]
    if b==0:
        postgres_insert_query1 = """ INSERT INTO  "Public".currency ("name") VALUES (%s)"""# insert
        cursor.execute(postgres_insert_query1, record_to_insert)


def currency1 (cursor,a):
    if type(a) is dict:
        for i in a:
            #print("currency1",i,a[i])
            if i == 'base' or i =='quote':
                f1 (cursor,a[i])
            if type(a[i]) is dict:
                currency1 (cursor,a[i])

try:
    conn = psycopg2.connect(dbname='daria', user='daria', password='dasha50', host='192.168.4.12', port='5432', )
    cursor = conn.cursor()
    postgres_delete_query1 = """ DELETE FROM "Public".symbols """
    cursor.execute(postgres_delete_query1)
    postgres_delete_query2 = """ DELETE FROM "Public".currency """
    cursor.execute(postgres_delete_query2)
    conn.commit()
    #print("deleted")

    g = ccxt.poloniex().load_markets()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(g)
    #print("ccxt got")
    currency1(cursor,g)
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

