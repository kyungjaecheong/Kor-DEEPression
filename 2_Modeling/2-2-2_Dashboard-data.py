'''
Looker Studio에서 직접 PostgreSQL로 서버 데이터를 이용하려 했었으나,
IP주소 할당 문제가 발생하여, csv로 변환후 대시보드를 제작하기로 함.
2-2-1_EDA.ipynb 에서 정한 변수들을 csv로 저장하여 대시보드 제작에 이용할 것임.

CLI 실행 명령어
$ python 2_Modeling/2-2-2_Dashboard-data.py
'''

# 라이브러리 및 함수 Import
import os
import sys
import psycopg2
from dotenv import load_dotenv
import pandas as pd

# .env파일에 저장된 정보들을 불러옴
load_dotenv(verbose=True)

# HOST, PORT, DATABASE, USERNAME, PASSWORD를 전역변수로 저장
HOST = os.getenv('postgre_host')
PORT = 5432
DATABASE = os.getenv('postgre_database')
USERNAME = os.getenv('postgre_user')
PASSWORD = os.getenv('postgre_password')

# 파일이 실행되면 자동으로 동작하는 main 함수
def main():
    
    # postgreSQL 연결
    try:
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USERNAME,
            password=PASSWORD)
        # 커서 지정
        cur = conn.cursor()
        print('\nconnection success to DB\n')
    
    # 예외처리 : 연결 실패할 경우 시스템을 중단
    except:
        print('\nconnection error to DB\n')
        sys.exit()

    # SQL Qurey문 정의 (변수는 EDA에서 정한 변수로 추출)
    sql_query = """
    SELECT f.id, y."year", f.age, 
        f.sex, f1.sex,
        f.household, f2.household,
        f.marital, f3.marital,
        f.subj_health, f4.subj_health,
        f.stress, f5.stress,
        t.depression, t.mdd
    FROM features AS f
    JOIN targets AS t ON f.id = t.id
    JOIN id_year AS y ON f.id = y.id
    JOIN sex AS f1 ON f.sex = f1.id_sex
    JOIN household AS f2 ON f.household = f2.id_household
    JOIN marital AS f3 ON f.marital = f3.id_marital
    JOIN subj_health AS f4 ON f.subj_health = f4.id_subj_health
    JOIN stress AS f5 ON f.stress = f5.id_stress
    """
    
    # 저장 경로 설정
    save_path_temp = './2_Modeling/downloads/temp_data/Dashboard_temp.csv'
    save_path_final = './2_Modeling/downloads/Dashboard_KorDEEP.csv'
    
    # csv 생성 SQL 쿼리문
    sql_csv = f"""COPY ({sql_query}) TO STDOUT WITH CSV DELIMITER ',';"""    
    with open(save_path_temp, 'w', encoding='utf-8') as cf:
        cur.copy_expert(sql_csv, cf)
        print("Temp file created Successfully")

    # postgreSQL 연결 종료
    conn.close()    
    print('\nSuccessfully Disconnected to DB\n')
    
    # Column 이름이 없는 상태로 저장되므로 다시 불러와서 Column 이름을 추가
    column_list = ['id', 'year', 'age', 'sex', '성별', 'household', '세대유형',
                   'marital', '혼인상태', 'subj_health', '주관적건강인지도',
                   'stress', '스트레스인지도', 'Depression', 'MDD']
    df_temp = pd.read_csv(save_path_temp, names=column_list)
    
    # Age column 범주화
    Ages = []
    for index, value in enumerate(df_temp.age):
        if value < 30:
            Ages.append('20s')
        elif value < 40:
            Ages.append('30s')
        elif value < 50:
            Ages.append('40s')
        elif value < 60:
            Ages.append('50s')
        elif value < 70:
            Ages.append('60s')
        elif value < 80:
            Ages.append('70s')
        else: Ages.append('over 80s')
    df_fix = df_temp.copy()
    df_fix['나이대'] = Ages
    
    # Depression 과 MDD를 종합한 Column을 새로 생성
    Depr_MDD_Code = []
    Depr_MDD_label = []
    for index in range(df_fix.shape[0]):
        if df_fix.loc[index, 'Depression'] == 0:
            Depr_MDD_Code.append(0)
            Depr_MDD_label.append('정상')
        elif df_fix.loc[index, 'MDD'] == 0:
            Depr_MDD_Code.append(1)
            Depr_MDD_label.append('경도우울증')
        elif df_fix.loc[index, 'MDD'] == 1:
            Depr_MDD_Code.append(2)
            Depr_MDD_label.append('주요우울장애')
    df_add_target = df_fix.copy()
    df_add_target['Depr_MDD'] = Depr_MDD_Code
    df_add_target['우울증분류'] = Depr_MDD_label
    
    # 열 순서 바꾸기
    sort_columns = ['id', 'year', 'age', '나이대', 'sex', '성별', 'household', '세대유형',
                   'marital', '혼인상태', 'subj_health', '주관적건강인지도', 'stress', '스트레스인지도', 
                   'Depression', 'MDD', 'Depr_MDD', '우울증분류']    
    df_sorted = df_add_target[sort_columns]
    
    # CSV file로 Export
    df_sorted.to_csv(save_path_final, index=False)    
    print("Column Addition & Saving csv : Success\n")
    
# 파일이 실행되면 자동으로 main 함수를 동작하도록 함  
if __name__ == '__main__':
    main()