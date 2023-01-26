import os
import sys
import csv
import psycopg2
from dotenv import load_dotenv

load_dotenv(verbose=True)

HOST = os.getenv('postgre_host')
PORT = 5432
DATABASE = os.getenv('postgre_database')
USERNAME = os.getenv('postgre_user')
PASSWORD = os.getenv('postgre_password')

def main():
    # postgreSQL 연결
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USERNAME,
            password=PASSWORD
        )
        cur = conn.cursor()
        print('connection success to DB')
    except:
        print('connection error to DB')
        sys.exit()
    
    # JOIN QUERY 1
    sql_query_join_1 = """
    SELECT f.*, t.depression
    FROM features f
    JOIN targets t
    ON f.id = t.id
    """
    
    # to csv 1
    sql_csv_1 = f"""COPY ({sql_query_join_1}) TO STDOUT WITH CSV DELIMITER ',';"""
    with open("./data/downloads/ver2/Depression.csv", "w") as cf:
        cur.copy_expert(sql_csv_1, cf)
    
    print("Depression.csv file created successfully")
    
    # JOIN QUERY 2
    sql_query_join_2 = """
    SELECT f.*, t.mdd
    FROM features f
    JOIN targets t
    ON f.id = t.id
    WHERE t.depression = 1
    """
    
    # to csv 2
    sql_csv_2 = f"""COPY ({sql_query_join_2}) TO STDOUT WITH CSV DELIMITER ',';"""
    with open("./data/downloads/ver2/MDD.csv", "w") as cf:
        cur.copy_expert(sql_csv_2, cf)
        
    print("MDD.csv file created successfully")    
    
    # JOIN QUERY 3
    sql_query_join_3 = """
    SELECT f.*, t.depression, t.mdd
    FROM features f
    JOIN targets t
    ON f.id = t.id
    """
    
    # to csv 3
    sql_csv_3 = f"""COPY ({sql_query_join_3}) TO STDOUT WITH CSV DELIMITER ',';"""
    with open("./data/downloads/ver2/MDD_Dep.csv", "w") as cf:
        cur.copy_expert(sql_csv_3, cf)
    
    conn.close()
    
    print('Successfully Disconnected to DB')

if __name__ == '__main__':
    main()