import psycopg2
import random
import string


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


try:
    conn = psycopg2.connect(dbname='daria', user='daria', password='dasha50', host='192.168.4.12', port='5432', )
    cursor = conn.cursor()
    postgres_delete_query1 = """ DELETE FROM "Public".symbols """
    cursor.execute(postgres_delete_query1)
    postgres_delete_query2 = """ DELETE FROM "Public".currency """
    cursor.execute(postgres_delete_query2)
    postgres_delete_query3 = """ DELETE FROM "Public".exchanges """
    cursor.execute(postgres_delete_query3)
    

    postgres_insert_query1 = """ INSERT INTO  "Public".currency ("name", description) VALUES (%s,%s)"""
    i=1
    while i<10:
        record_to_insert = (randomString(10), randomString(10))
        cursor.execute(postgres_insert_query1, record_to_insert)  
        i+=1

    postgres_insert_query2 = """ INSERT INTO  "Public".exchanges ("name") VALUES (%s)"""
    i=1
    while i<10:
        record_to_insert = (randomString(10),)
        cursor.execute(postgres_insert_query2, record_to_insert)  
        i+=1  
    postgres_select_query = """select id from "Public".currency"""
    cursor.execute(postgres_select_query)
    a = cursor.fetchall()
    #print(a)
    postgres_insert_query3 = """ INSERT INTO "Public".symbols (base_id, quote_id) VALUES (%s,%s)"""
    for i in a:
        for j in a:
            if i<j:
                record_to_insert = (i, j)
                cursor.execute(postgres_insert_query3, record_to_insert)
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

    
