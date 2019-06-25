import ccxt
import pprint
import psycopg2

# The function for checking the presence of currency's name into table and insert new one.
def insert_into_currency(cursor,curr) :
    postgres_select_query = """ SELECT count(*) cnt FROM "Public".currency WHERE "name"= %s """# check record
    record_to_insert = (curr,)
    cursor.execute(postgres_select_query,record_to_insert)
    c = cursor.fetchall()
    b = c[0][0]
    if b==0:
        postgres_insert_query1 = """ INSERT INTO  "Public".Currency ("name") VALUES (%s)"""# insert
        cursor.execute(postgres_insert_query1, record_to_insert)

# The function for receiving currency's name from market.
def receiving_currency(cursor,a):
    if type(a) is dict:
        for key in a:
            if type(a[key]) is str and (key == 'base' or key =='quote'):
                #print (a[key])
                insert_into_currency(cursor,a[key])
            if type(a[key]) is dict:
                receiving_currency(cursor,a[key])

# The function for insert currency's id from table Currency into table Symbols.    
def inset_into_symbols(cursor,market):
    postgres_select_query = """Select id,name from "Public".Currency"""
    cursor.execute(postgres_select_query)
    a = cursor.fetchall()
    id_from_currency = {} 
    for iterator in a:
        id_from_currency[iterator[1]]=iterator[0]
    for iterator in market:
        currency= iterator.split('/')
        if len(currency)==2:
            base_id=id_from_currency[currency[0]]
            quote_id=id_from_currency[currency[1]]
            postgres_insert_query1 = """ INSERT INTO  "Public".Symbols ("base_id","quote_id") VALUES (%s,%s)"""# insert
            record_to_insert = (base_id,quote_id)
            cursor.execute(postgres_insert_query1, record_to_insert)

try:
    connection = psycopg2.connect(dbname='daria', user='daria', password='dasha50', host='192.168.4.12', port='5432', )
    cursor = connection.cursor()
    postgres_delete_query1 = """ DELETE FROM "Public".Symbols """
    cursor.execute(postgres_delete_query1)
    postgres_delete_query2 = """ DELETE FROM "Public".Currency """
    cursor.execute(postgres_delete_query2)
    connection.commit()
    
    kraken_market = ccxt.kraken().load_markets()
    #pp = pprint.PrettyPrinter()
    #pp.pprint(kraken_market)
    receiving_currency(cursor,kraken_market)
    inset_into_symbols(cursor,kraken_market)
    connection.commit()

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed", error)
finally:
    #closing database connection.
    if(connection):
        if (cursor):
            cursor.close()
        connection.close()
    print("PostgreSQL connection is closed")

