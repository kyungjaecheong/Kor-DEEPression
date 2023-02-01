'''
Custom Module for Step 1-2 PostgreSQL DataBase

Project(Step) : Kor-Deepression (Step_1 : DataBase)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

# 함수 리스트 및 __all__ 정의(import * 할 때 불러올 함수들을 정의)
# from custom_modules.preprocess import *
__all__ = ['table_initialization',
           'table_creation',
           'insertion_csv',
           'insertion_json']

# 라이브러리 import
import csv
import json

# 테이블 초기화 기능(features-->범주형변수들-->targets-->id_year)
# 외래키를 가진 테이블(자식)부터 제거해야하므로 순서가 중요함
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
    
    # 입력 받은 table list의 역순으로 반복을 진행함
    for table_name in reversed(table_list):
        # 테이블 이름과 동일한 테이블이 존재하면 삭제하는 명령어 실행 
        cursor.execute(f"""DROP TABLE IF EXISTS {table_name};""")


# 테이블 생성 기능(id_year-->targets-->범주형변수들-->features)
# 외래키를 가지지 않는 테이블(부모)부터 생성해야하므로 순서가 중요함
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
    
    # id_year 테이블 생성 (부모 테이블)
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_list[0]} (
        id VARCHAR NOT NULL,
        year INTEGER,
        CONSTRAINT {table_list[0]}_pk PRIMARY KEY (id)
        );""")
    
    # targets 테이블 생성 (id_year의 자식 테이블)
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_list[1]} (
        id VARCHAR NOT NULL,
        depression INTEGER,
        mdd INTEGER,
        CONSTRAINT {table_list[1]}_pk PRIMARY KEY (id),
        CONSTRAINT {table_list[1]}_fk FOREIGN KEY (id) REFERENCES {table_list[0]} (id)
        );""")
    
    # 범주형 변수들(총 10개)의 테이블들을 생성 (부모 테이블)
    for feature_name in table_list[2:-1]:
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {feature_name} (
            id_{feature_name} INTEGER,
            {feature_name} VARCHAR,
            CONSTRAINT {feature_name}_pk PRIMARY KEY (id_{feature_name})
            );""")
    
    # features 테이블 생성 (id_year와 범주형 테이블들의 자식 테이블)
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


# csv data를 RDB에 입력하는 기능
# csv에서 한줄씩 넣는 executemany 방식은 시간이 상당히 오래 걸림
# cursor의 copy_from 메소드로 csv전체를 복사하여 RDB에 붙여 넣으면 훨씬 간단하고 빠르게 수행할 수 있음!
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
    # 연산 실시후 파일이 닫히도록 with문을 활용한다
    with open(path, 'r') as cf:
        # csv 모듈의 reader를 통해 csv 파일을 읽기
        csv_reader = csv.reader(cf)
        # 첫 행에는 변수 이름이 저장되어 있으므로 next로 넘어가기
        next(csv_reader)
        # copy_from으로 csv데이터를 통째로 입력하기
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
    # 연산 실시후 파일이 닫히도록 with문을 활용한다
    with open(path, 'r', encoding='utf-8') as jf:
        json_reader = json.load(jf)
    # 전달받은 table list의 요소를 순서대로 반복하여 json 데이터를 입력
    for table_name in table_list:
        cursor.executemany(f"""INSERT INTO {table_name} (id_{table_name}, {table_name}) VALUES (%s, %s);""",
                           [list(dict.values()) for dict in json_reader[table_name]])