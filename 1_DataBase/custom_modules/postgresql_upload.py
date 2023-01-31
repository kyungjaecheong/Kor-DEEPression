'''
Custom Module for Step 1-2 PostgreSQL DataBase

Project(Step) : Kor-Deepression (Step_1 : DataBase)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

import csv
import json

def table_initialization(cursor, table_list):
    '''
    table_initialization
        테이블 초기화 기능
    ---
    입력 변수 정보
        cursor : (object) psycopg2.connect.cursor()
        table_list : (list) 테이블 이름 리스트
    ---
    출력 : None 
    '''
    for table_name in reversed(table_list):
        cursor.execute(f"""DROP TABLE IF EXISTS {table_name};""")


def table_creation(cursor, table_list):
    '''
    table_creation
        테이블 생성 기능
    ---
    입력 변수 정보
        cursor : (object) psycopg2.connect.cursor()
        table_list : (list) 테이블 이름 리스트
    ---
    출력 : None 
    '''

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_list[0]} (
        id VARCHAR NOT NULL,
        year INTEGER,
        CONSTRAINT {table_list[0]}_pk PRIMARY KEY (id)
        );""")
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_list[1]} (
        id VARCHAR NOT NULL,
        depression INTEGER,
        mdd INTEGER,
        CONSTRAINT {table_list[1]}_pk PRIMARY KEY (id),
        CONSTRAINT {table_list[1]}_fk FOREIGN KEY (id) REFERENCES {table_list[0]} (id)
        );""")
    for feature_name in table_list[2:-1]:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {feature_name} (
            id_{feature_name} INTEGER,
            {feature_name} VARCHAR,
            CONSTRAINT {feature_name}_pk PRIMARY KEY (id_{feature_name})
            );""")
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_list[-1]} (
        id VARCHAR NOT NULL,
        age INTEGER,
        bmi FLOAT,
        {table_list[2]} INTEGER,
        {table_list[3]} INTEGER,
        {table_list[4]} INTEGER,
        {table_list[5]} INTEGER,
        {table_list[6]} INTEGER,
        {table_list[7]} INTEGER,
        limitation INTEGER,
        modality INTEGER,
        w_change INTEGER,
        high_bp INTEGER,
        diabetes INTEGER,
        dyslipidemia INTEGER,
        {table_list[-5]} INTEGER,
        {table_list[-4]} INTEGER,
        {table_list[-3]} INTEGER,
        {table_list[-2]} INTEGER,
        CONSTRAINT {table_list[-1]}_pk PRIMARY KEY (id),
        CONSTRAINT {table_list[-1]}_fk FOREIGN KEY (id) REFERENCES {table_list[0]} (id),
        CONSTRAINT {table_list[-1]}_fk_{table_list[2]} FOREIGN KEY ({table_list[2]}) REFERENCES {table_list[2]} (id_{table_list[2]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[3]} FOREIGN KEY ({table_list[3]}) REFERENCES {table_list[3]} (id_{table_list[3]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[4]} FOREIGN KEY ({table_list[4]}) REFERENCES {table_list[4]} (id_{table_list[4]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[5]} FOREIGN KEY ({table_list[5]}) REFERENCES {table_list[5]} (id_{table_list[5]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[6]} FOREIGN KEY ({table_list[6]}) REFERENCES {table_list[6]} (id_{table_list[6]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[7]} FOREIGN KEY ({table_list[7]}) REFERENCES {table_list[7]} (id_{table_list[7]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[-5]} FOREIGN KEY ({table_list[-5]}) REFERENCES {table_list[-5]} (id_{table_list[-5]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[-4]} FOREIGN KEY ({table_list[-4]}) REFERENCES {table_list[-4]} (id_{table_list[-4]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[-3]} FOREIGN KEY ({table_list[-3]}) REFERENCES {table_list[-3]} (id_{table_list[-3]}),
        CONSTRAINT {table_list[-1]}_fk_{table_list[-2]} FOREIGN KEY ({table_list[-2]}) REFERENCES {table_list[-2]} (id_{table_list[-2]})
        );""")

def insertion_csv(cursor, table_name, path):
    '''
    insertion_csv
        csv data를 RDB에 입력하는 기능
    ---
    입력 변수 정보
        cursor : (object) psycopg2.connect.cursor()
        table_name : (str) 테이블 이름
        path : csv file 디렉토리
    ---
    출력 : None 
    '''
    with open(path, 'r') as cf:
        csv_reader = csv.reader(cf)
        next(csv_reader)
        cursor.copy_from(cf, table_name, sep=',')

def insertion_json(cursor, table_list, path):
    '''
    insertion_json
        json data를 RDB에 입력하는 기능
    ---
    입력 변수 정보
        cursor : (object) psycopg2.connect.cursor()
        table_list : (list) 테이블 이름 리스트
        path : json file 디렉토리
    ---
    출력 : None 
    '''
    with open(path, 'r', encoding='utf-8') as jf:
        json_reader = json.load(jf)
    for table_name in table_list:
        cursor.executemany(f"""INSERT INTO {table_name} (id_{table_name}, {table_name}) VALUES (%s, %s);""",
                           [list(dict.values()) for dict in json_reader[table_name]])