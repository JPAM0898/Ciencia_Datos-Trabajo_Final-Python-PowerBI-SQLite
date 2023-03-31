import sqlite3
import pandas as pd

# Create database
def database(df,indice, DBMS_Path):
    BD = []
    try:
        conn = sqlite3.connect(DBMS_Path)
        BD = df.to_sql('BDrun{}'.format(indice+1), conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        print(e)
    return BD
