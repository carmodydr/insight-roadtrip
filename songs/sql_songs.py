## Python packages - you may have to pip install sqlalchemy, sqlalchemy_utils, and psycopg2.
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd
import MySQLdb as mdb

#In Python: Define a database name (we're using a dataset on births, so I call it 
# birth_db), and your username for your computer (CHANGE IT BELOW). 
dbname = 'birth_db'
username = 'dan'
pswd = 'insight'

## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('mysql://%s:%s@localhost/%s'%(username,pswd,dbname))
print engine.url
# Replace localhost with IP address if accessing a remote server

## create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

# load a database from CSV
birth_data = pd.DataFrame.from_csv('births2012_downsampled.csv')

## insert data into database from Python (proof of concept - this won't be useful for big data, of course)
## df is any pandas dataframe 
birth_data.to_sql('birth_data_table', engine, if_exists='replace')


## Now try the same queries, but in python!

# connect:
con = None
con = mdb.connect('localhost', username, pswd, dbname)

# query:
sql_query = """
SELECT * FROM birth_data_table WHERE delivery_method='Cesarean';
"""
birth_data_from_sql = pd.read_sql_query(sql_query,con)

birth_data_from_sql.head()
