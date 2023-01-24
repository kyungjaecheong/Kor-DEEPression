import os
import sys
import csv
import json
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
            password=PASSWORD)
        cur = conn.cursor()
        print('connection success to DB')
    except:
        print('connection error to DB')
        sys.exit()

    # 테이블 초기화
    cur.execute("""DROP TABLE IF EXISTS targets;""")
    cur.execute("""DROP TABLE IF EXISTS features;""")
    cur.execute("""DROP TABLE IF EXISTS sex;""")
    cur.execute("""DROP TABLE IF EXISTS education;""")
    cur.execute("""DROP TABLE IF EXISTS generation;""")
    cur.execute("""DROP TABLE IF EXISTS marital;""")
    cur.execute("""DROP TABLE IF EXISTS economy;""")
    cur.execute("""DROP TABLE IF EXISTS subj_health;""")
    cur.execute("""DROP TABLE IF EXISTS limitation;""")
    cur.execute("""DROP TABLE IF EXISTS modality;""")
    cur.execute("""DROP TABLE IF EXISTS w_change;""")
    cur.execute("""DROP TABLE IF EXISTS w_control;""")
    cur.execute("""DROP TABLE IF EXISTS drk_freq;""")
    cur.execute("""DROP TABLE IF EXISTS drk_amount;""")
    cur.execute("""DROP TABLE IF EXISTS smoke;""")
    cur.execute("""DROP TABLE IF EXISTS stress;""")
    cur.execute("""DROP TABLE IF EXISTS id_year;""")
    print('table initialization complete')
    
    # 테이블 생성
    sql_create_table_idy = """CREATE TABLE IF NOT EXISTS id_year (
        id VARCHAR NOT NULL,
        year INTEGER,
        CONSTRAINT id_year_pk PRIMARY KEY (id)
        );"""
    sql_create_table_targ = """CREATE TABLE IF NOT EXISTS targets (
        id VARCHAR NOT NULL,
        depression INTEGER,
        mdd INTEGER,
        CONSTRAINT targets_pk PRIMARY KEY (id),
        CONSTRAINT targets_fk FOREIGN KEY (id) REFERENCES id_year (id)
        );"""
    sql_create_table_sex = """CREATE TABLE IF NOT EXISTS sex (
        sex INTEGER,
        name VARCHAR,
        CONSTRAINT sex_pk PRIMARY KEY (sex)
        );"""
    sql_create_table_education = """CREATE TABLE IF NOT EXISTS education (
        education INTEGER,
        name VARCHAR,
        CONSTRAINT education_pk PRIMARY KEY (education)
        );"""
    sql_create_table_generation = """CREATE TABLE IF NOT EXISTS generation (
        generation INTEGER,
        name VARCHAR,
        CONSTRAINT generation_pk PRIMARY KEY (generation)
        );"""
    sql_create_table_marital = """CREATE TABLE IF NOT EXISTS marital (
        marital INTEGER,
        name VARCHAR,
        CONSTRAINT marital_pk PRIMARY KEY (marital)
        );"""
    sql_create_table_economy = """CREATE TABLE IF NOT EXISTS economy (
        economy INTEGER,
        name VARCHAR,
        CONSTRAINT economy_pk PRIMARY KEY (economy)
        );"""
    sql_create_table_subj_health = """CREATE TABLE IF NOT EXISTS subj_health (
        subj_health INTEGER,
        name VARCHAR,
        CONSTRAINT subj_health_pk PRIMARY KEY (subj_health)
        );"""
    sql_create_table_limitation = """CREATE TABLE IF NOT EXISTS limitation (
        limitation INTEGER,
        name VARCHAR,
        CONSTRAINT limitation_pk PRIMARY KEY (limitation)
        );"""
    sql_create_table_modality = """CREATE TABLE IF NOT EXISTS modality (
        modality INTEGER,
        name VARCHAR,
        CONSTRAINT modality_pk PRIMARY KEY (modality)
        );"""
    sql_create_table_w_change = """CREATE TABLE IF NOT EXISTS w_change (
        w_change INTEGER,
        name VARCHAR,
        CONSTRAINT w_change_pk PRIMARY KEY (w_change)
        );"""
    sql_create_table_w_control = """CREATE TABLE IF NOT EXISTS w_control (
        w_control INTEGER,
        name VARCHAR,
        CONSTRAINT w_control_pk PRIMARY KEY (w_control)
        );"""
    sql_create_table_drk_freq = """CREATE TABLE IF NOT EXISTS drk_freq (
        drk_freq INTEGER,
        name VARCHAR,
        CONSTRAINT drk_freq_pk PRIMARY KEY (drk_freq)
        );"""
    sql_create_table_drk_amount = """CREATE TABLE IF NOT EXISTS drk_amount (
        drk_amount INTEGER,
        name VARCHAR,
        CONSTRAINT drk_amount_pk PRIMARY KEY (drk_amount)
        );"""
    sql_create_table_smoke = """CREATE TABLE IF NOT EXISTS smoke (
        smoke INTEGER,
        name VARCHAR,
        CONSTRAINT smoke_pk PRIMARY KEY (smoke)
        );"""
    sql_create_table_stress = """CREATE TABLE IF NOT EXISTS stress (
        stress INTEGER,
        name VARCHAR,
        CONSTRAINT stress_pk PRIMARY KEY (stress)
        );"""
    sql_create_table_feat = """CREATE TABLE IF NOT EXISTS features (
        id VARCHAR NOT NULL,
        age INTEGER,
        bmi FLOAT,
        sex INTEGER,
        education INTEGER,
        generation INTEGER,
        marital INTEGER,
        economy INTEGER,
        subj_health INTEGER,
        limitation INTEGER,
        modality INTEGER,
        w_change INTEGER,
        w_control INTEGER,
        drk_freq INTEGER,
        drk_amount INTEGER,
        smoke INTEGER,
        stress INTEGER,
        CONSTRAINT features_pk PRIMARY KEY (id),
        CONSTRAINT features_fk FOREIGN KEY (id) REFERENCES id_year (id),
        CONSTRAINT features_fk_sex FOREIGN KEY (sex) REFERENCES sex (sex),
        CONSTRAINT features_fk_education FOREIGN KEY (education) REFERENCES education (education),
        CONSTRAINT features_fk_generation FOREIGN KEY (generation) REFERENCES generation (generation),
        CONSTRAINT features_fk_marital FOREIGN KEY (marital) REFERENCES marital (marital),
        CONSTRAINT features_fk_economy FOREIGN KEY (economy) REFERENCES economy (economy),
        CONSTRAINT features_fk_subj_health FOREIGN KEY (subj_health) REFERENCES subj_health (subj_health),
        CONSTRAINT features_fk_limitation FOREIGN KEY (limitation) REFERENCES limitation (limitation),
        CONSTRAINT features_fk_modality FOREIGN KEY (modality) REFERENCES modality (modality),
        CONSTRAINT features_fk_w_change FOREIGN KEY (w_change) REFERENCES w_change (w_change),
        CONSTRAINT features_fk_w_control FOREIGN KEY (w_control) REFERENCES w_control (w_control),
        CONSTRAINT features_fk_drk_freq FOREIGN KEY (drk_freq) REFERENCES drk_freq (drk_freq),
        CONSTRAINT features_fk_drk_amount FOREIGN KEY (drk_amount) REFERENCES drk_amount (drk_amount),
        CONSTRAINT features_fk_smoke FOREIGN KEY (smoke) REFERENCES smoke (smoke),
        CONSTRAINT features_fk_stress FOREIGN KEY (stress) REFERENCES stress (stress)
        );"""
    
    cur.execute(sql_create_table_idy)
    cur.execute(sql_create_table_sex)
    cur.execute(sql_create_table_education)
    cur.execute(sql_create_table_generation)
    cur.execute(sql_create_table_marital)
    cur.execute(sql_create_table_economy)
    cur.execute(sql_create_table_subj_health)
    cur.execute(sql_create_table_limitation)
    cur.execute(sql_create_table_modality)
    cur.execute(sql_create_table_w_change)
    cur.execute(sql_create_table_w_control)
    cur.execute(sql_create_table_drk_freq)
    cur.execute(sql_create_table_drk_amount)
    cur.execute(sql_create_table_smoke)
    cur.execute(sql_create_table_stress)
    cur.execute(sql_create_table_feat)
    cur.execute(sql_create_table_targ)
    print('table created complete')
    
    with open('./data/downloads/HN_year.csv', 'r') as cf:
        csv_reader = csv.reader(cf)
        next(csv_reader)
        cur.copy_from(cf, 'id_year', sep=',')    
    
    with open('./data/variable_info.json', 'r', encoding='utf-8') as jf:
        json_reader = json.load(jf)
    list_sex = [list(dict.values()) for dict in json_reader['sex']]
    list_edu = [list(dict.values()) for dict in json_reader['education']]
    list_gen = [list(dict.values()) for dict in json_reader['generation']]
    list_mari = [list(dict.values()) for dict in json_reader['marital']]
    list_econ = [list(dict.values()) for dict in json_reader['economy']]
    list_health = [list(dict.values()) for dict in json_reader['subj_health']]
    list_limit = [list(dict.values()) for dict in json_reader['limitation']]
    list_modal = [list(dict.values()) for dict in json_reader['modality']]
    list_wchan = [list(dict.values()) for dict in json_reader['w_change']]
    list_wcon = [list(dict.values()) for dict in json_reader['w_control']]
    list_drkfreq = [list(dict.values()) for dict in json_reader['drk_freq']]
    list_drkamt = [list(dict.values()) for dict in json_reader['drk_amount']]
    list_smoke = [list(dict.values()) for dict in json_reader['smoke']]
    list_stress = [list(dict.values()) for dict in json_reader['stress']]
    cur.executemany("""INSERT INTO sex (sex, name) VALUES (%s, %s);""", list_sex)
    cur.executemany("""INSERT INTO education (education, name) VALUES (%s, %s);""", list_edu)
    cur.executemany("""INSERT INTO generation (generation, name) VALUES (%s, %s);""", list_gen)
    cur.executemany("""INSERT INTO marital (marital, name) VALUES (%s, %s);""", list_mari)
    cur.executemany("""INSERT INTO economy (economy, name) VALUES (%s, %s);""", list_econ)
    cur.executemany("""INSERT INTO subj_health (subj_health, name) VALUES (%s, %s);""", list_health)
    cur.executemany("""INSERT INTO limitation (limitation, name) VALUES (%s, %s);""", list_limit)
    cur.executemany("""INSERT INTO modality (modality, name) VALUES (%s, %s);""", list_modal)
    cur.executemany("""INSERT INTO w_change (w_change, name) VALUES (%s, %s);""", list_wchan)
    cur.executemany("""INSERT INTO w_control (w_control, name) VALUES (%s, %s);""", list_wcon)
    cur.executemany("""INSERT INTO drk_freq (drk_freq, name) VALUES (%s, %s);""", list_drkfreq)
    cur.executemany("""INSERT INTO drk_amount (drk_amount, name) VALUES (%s, %s);""", list_drkamt)
    cur.executemany("""INSERT INTO smoke (smoke, name) VALUES (%s, %s);""", list_smoke)
    cur.executemany("""INSERT INTO stress (stress, name) VALUES (%s, %s);""", list_stress)
        
    with open('./data/downloads/HN_feature.csv', 'r') as cf:
        csv_reader = csv.reader(cf)
        next(csv_reader)
        cur.copy_from(cf, 'features', sep=',')
        
    with open('./data/downloads/HN_target.csv', 'r') as cf:
        csv_reader = csv.reader(cf)
        next(csv_reader)
        cur.copy_from(cf, 'targets', sep=',')
        
    print('data insert complete')

    conn.commit()
    conn.close()
    
    print('Successfully Disconnected to DB')
    
if __name__ == '__main__':
    main()