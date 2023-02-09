'''
Custom Module for Step 1-1 Data Prepare

Project(Step) : Kor-Deepression (Step_1 : DataBase)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

# 함수 리스트 및 __all__ 정의(import * 할 때 불러올 함수들을 정의)
# from custom_modules.preprocess import *
__all__ = ['data_load',
           'data_load_20',
           'concat_df',
           'drop_nan_df',
           'drop_9s_df',
           'get_targets',
           'get_features',
           'devide_for_RDB']

# 라이브러리 import 
import pandas as pd


# column 리스트 정의(기본변수, 건강설문, 생활습관, 만성질환, 우울증변수)
col_demo = ['year', 'age', 'HE_BMI', 'sex', 'edu', 'genertn', 'marri_2', 'EC1_1']
col_health = ['D_1_1', 'LQ4_00', 'D_2_1', 'BO1_1', 'BO2_1']
col_life = ['BD1_11', 'BD2_1', 'sm_presnt', 'BP1']
col_disease = ['HE_HP', 'HE_DM', 'HE_HCHOL', 'HE_HTG']
col_disease_20 = ['HE_HP', 'HE_DM_HbA1c', 'HE_HCHOL', 'HE_HTG']
col_dpr = ['DF2_pr', 'mh_PHQ_S']


# 데이터 불러오기 기능(2014, 2016, 2018)
def data_load(filedir):
    '''
    data_load
        데이터 불러오기 기능(2014, 2016, 2018)
    ---
    입력 변수 정보
        filedir : (str)불러올 파일의 디렉토리
    ---
    출력 : DataFrame 
    '''
    # csv file 불러오기(여러 type이 섞여있는 column도 있으므로 low_memory=False로 설정)
    df0 = pd.read_csv(filedir, low_memory=False)
    # 분석에 이용할 column list를 정의(리스트 합 연산)
    col_list = ['id']+col_demo+col_health+col_disease+col_life+col_dpr
    # column list에 해당하는 column을 추출
    df1 = df0[col_list]
    # column을 추출한 DataFrame 출력
    return df1


# 데이터 불러오기 기능(2020)
def data_load_20(filedir):
    '''
    data_load
        데이터 불러오기 기능(2020)
    ---
    입력 변수 정보
        filedir : (str)불러올 파일의 디렉토리
    ---
    출력 : DataFrame
    '''
    # csv file 불러오기(여러 type이 섞여있는 column도 있으므로 low_memory=False로 설정)
    df0 = pd.read_csv(filedir, low_memory=False)
    # 분석에 이용할 column list를 정의(리스트 합 연산)
    col_list = ['ID']+col_demo+col_health+col_disease_20+col_life+col_dpr
    # column list에 해당하는 column을 추출 및 column 이름을 통일시키기
    df1 = df0[col_list].rename(columns={'ID':'id','HE_DM_HbA1c':'HE_DM'})
    # column을 추출한 DataFrame 출력
    return df1


# 데이터 병합 기능(concatenate)
def concat_df(df_list):
    '''
    concat_df
        데이터 병합 기능 (row 방향)
    ---
    입력 변수 정보
        df_list : (list)병합할 DataFrame의 List
    ---
    출력 : DataFrame
    '''
    # concat(default는 row 방향, index 초기화를 위해 ignore_index=True로 설정)
    df = pd.concat(df_list, ignore_index=True)
    # 병합한 DataFrame 출력
    return df


# 결측치 제거 기능 : 결측치는 ' '(공백)으로 채워져 있음
def drop_nan_df(df):
    '''
    drop_nan_df
        결측치 제거 기능 (결측치는 ' '(공백)으로 채워져 있음)
    ---
    입력 변수 정보
        df : (DataFrame)결측치 제거할 DataFrame
    ---
    출력 : 결측치 제거 후 DataFrame
    '''
    # 공백(' ')을 None값으로 변환하는 함수 정의
    def fill_nan(value):
        if value == ' ':
            value = None
        return value
    # 원본 데이터 변환 방지를 위해 copy 실시
    df1 = df.copy()
    # applymap으로 모든 데이터 값에 변환 함수를 적용
    df1 = df1.applymap(fill_nan)
    # 결측치가 하나라도 존재(any)하면 row(axis=0)를 제거
    df1 = df1.dropna(axis=0, how='any')
    # 결측치 제거한 DataFrame 출력
    return df1


# 결측치 제거 기능 2 : 설문변수중에서 응답을 거부하거나 모르겠다고 응답한 경우(9 or 99)
# csv editor를 통해 직접 확인하여 제거를 진행하였으며, 제거는 query함수로 실시함
def drop_9s_df(df):
    '''
    drop_9s_df
        설문변수 무응답 데이터(결측치) 제거 기능 (9 또는 99)
    ---
    입력 변수 정보
        df : (DataFrame)결측치 제거할 DataFrame
    ---
    출력 : 결측치 제거 후 DataFrame
    '''
    # marri_2(결혼상태), D_1_1(주관적건강인지)
    df1 = df.query('marri_2!=99 and marri_2!=8 and marri_2!=9 and D_1_1!=9')
    # BO1_1(연간체중변화), BD1_11(연간음주빈도), BD2_1(1회음주량), BP1(스트레스인지정도)
    df2 = df1.query('BO1_1!=9 and BD1_11!=9 and BD2_1!=9 and BP1!=9')
    # index reset
    df2 = df2.reset_index(drop=True)
    # 결측치 제거한 DataFrame 출력
    return df2


# Target으로 쓸 Column을 추가하는 기능
def get_targets(df):
    '''
    get_targets
        Target으로 쓸 Column을 추가하는 기능
    ---
    입력 변수 정보
        df : (DataFrame) DataFrame
    ---
    출력 : target column을 추가한 DataFrame
    '''
    # 빈 리스트 생성
    depression = []
    MDD = []
    # 우울증 관련 변수만 추출하기
    df_targets = df[col_dpr]    # ['DF2_pr', 'mh_PHQ_S']
    # DataFrame의 row 한줄씩 반복 수행
    for i in range(len(df_targets)):
        # 우울증을 현재 가지고 있다고 응답 or PHQ-9점수가 5점 이상인 경우
        if df_targets.loc[i, 'DF2_pr'] == 1\
        or df_targets.loc[i, 'mh_PHQ_S'] > 4:
            # Depression = 1
            depression.append(1)
            # PHQ-9점수가 10점 이상인 경우 : 주요우울장애(MDD)로 구분
            if df_targets.loc[i, 'mh_PHQ_S'] > 9:
                MDD.append(1)
            else:
                MDD.append(0)
        # 우울증 의사진단 받지 않거나(8) 현재 우울증이 없으며(0), PHQ-9점수도 4점 이하
        else:
            # Depression & MDD = 0
            depression.append(0)
            MDD.append(0)
    # Target Column 추가
    df['Depression'] = depression
    df['MDD'] = MDD
    # target column을 추가한 DataFrame 출력
    return df


# Feature 1차 가공(재분류)
def get_features(df):
    '''
    get_features
        가공한 Feature의 Column을 추가하는 기능
    ---
    입력 변수 정보
        df : (DataFrame) DataFrame
    ---
    출력 : 가공한 Feature column을 추가한 DataFrame
    '''
    # 빈 리스트 생성
    household = []
    marital = []
    limit = []
    modality = []
    w_change = []
    HE_HBP = []
    HE_DB = []
    HE_DYSL = []
    drink_freq = []
    drink_amount = []
    
    # DataFrame의 row 한줄씩 반복 수행
    for i in range(len(df)):
        
        # 가구 세대 구성 (1~7) --> household (0~3)
        # 1인 가구 (1)
        if df.loc[i, 'genertn'] == 1:
            household.append(0)
        # 1세대 가구 (2,3)
        elif df.loc[i, 'genertn'] in [2,3]:
            household.append(1)
        # 2세대 가구 (4,5,6)
        elif df.loc[i, 'genertn'] in [4,5,6]:
            household.append(2)
        # 3세대 이상 가구 (7)
        elif df.loc[i, 'genertn'] == 7:
            household.append(3)
        
        # 결혼 상태(1~4,88) --> marital(1~3)
        # 기혼 및 유배우자 (1,2)
        if df.loc[i, 'marri_2'] in [1,2]:
            marital.append(1)
        # 사별 혹은 이혼 (3,4)
        elif df.loc[i, 'marri_2'] in [3,4]:
            marital.append(2)
        # 미혼(88)
        elif df.loc[i, 'marri_2'] == 88:
            marital.append(3)
        
        # 질환 및 사고에 의한 활동 제한 여부
        # 아니오(2) --> 0
        if df.loc[i, 'LQ4_00'] == 2:
            limit.append(0)
        # 예(1) --> 1
        elif df.loc[i, 'LQ4_00'] == 1:
            limit.append(1)
        
        # 2주간 이환(질환) 여부
        # 아니오(2) --> 0
        if df.loc[i, 'D_2_1'] == 2:
            modality.append(0)
        # 예(1) --> 1
        elif df.loc[i, 'D_2_1'] == 1:
            modality.append(1)
        
        # 1년간 체중 조절 노력 없이 체중이 3kg이상 변화한 경우
        # 체중변화없음(1) --> 0
        if df.loc[i, 'BO1_1'] == 1:
            w_change.append(0)
        # 체중감소(2)or체중증가(3) & 체중 조절 노력함(1,2,3) --> 0
        elif df.loc[i, 'BO1_1'] in [2,3]\
        and df.loc[i, 'BO2_1'] in [1,2,3]:
            w_change.append(0)
        # 체중감소(2)or체중증가(3) & 체중 조절 노력 안함(4) --> 1
        elif df.loc[i, 'BO1_1'] in [2,3]\
        and df.loc[i, 'BO2_1'] == 4:
            w_change.append(1)
        
        # 고혈압 유병 여부
        # 고혈압(3) --> 1        
        if df.loc[i, 'HE_HP'] == 3:
            HE_HBP.append(1)
        # 정상(1), 전단계(2) --> 0
        elif df.loc[i, 'HE_HP'] in [1,2]:
            HE_HBP.append(0)
        
        # 당뇨병 유병 여부
        # 당뇨병(3) --> 1
        if df.loc[i, 'HE_DM'] == 3:
            HE_DB.append(1)
        # 정상(1), 공복혈당장애(2) --> 0
        elif df.loc[i, 'HE_DM'] in [1,2]:
            HE_DB.append(0)
        
        # 이상지질혈증(고지혈증) 유병 여부
        # 고콜레스테롤혈증(1) or 고중성지방혈증(1) --> 1
        if df.loc[i, 'HE_HCHOL'] == 1\
        or df.loc[i, 'HE_HTG'] == 1:
            HE_DYSL.append(1)
        # 모두 정상(0) --> 0
        elif df.loc[i, 'HE_HCHOL'] == 0\
        and df.loc[i, 'HE_HTG'] == 0:
            HE_DYSL.append(0)
        
        # 1년간 음주 빈도 (1~6, 8) --> (0~6)
        # 평생마셔본적없음(8) --> 0
        if df.loc[i, 'BD1_11'] == 8:
            drink_freq.append(0)
        # 나머지 변수(1~6) 그대로 사용
        elif df.loc[i, 'BD1_11'] in [1,2,3,4,5,6]:
            drink_freq.append(df.loc[i, 'BD1_11'])
        
        # 1회 음주량 (1~5, 8) --> (0~5)
        # 1년간 안마심(8) or 평생 안마심(8) --> 0
        if df.loc[i, 'BD2_1'] == 8:
            drink_amount.append(0)
        # 나머지 변수(1~5) 그대로 사용
        elif df.loc[i, 'BD2_1'] in [1,2,3,4,5]:
            drink_amount.append(df.loc[i, 'BD2_1'])
    
    # 가공한 Feature의 Column을 추가
    df['household'] = household
    df['marital'] = marital
    df['limit'] = limit
    df['modality'] = modality
    df['w_change'] = w_change
    df['HE_HBP'] = HE_HBP
    df['HE_DB'] = HE_DB
    df['HE_DYSL'] = HE_DYSL
    df['dr_freq'] = drink_freq
    df['dr_amount'] = drink_amount
    # 가공한 Feature column을 추가한 DataFrame 출력
    return df


# 가공한 DataFrame을 RDB형태에 맞도록 재조합하는 기능
def devide_for_RDB(df):
    '''
    devide_for_RDB
        가공한 DataFrame을 RDB형태에 맞도록 재조합하는 기능
    ---
    입력 변수 정보
        df : (DataFrame) 분리 할 DataFrame의 List
    ---
    출력 : tuple of DataFrame
    '''
    # 변수 리스트 정의
    col_year = ['id', 'year']
    col_feature = ['id', 'age', 'HE_BMI', 'sex', 'edu',
                   'household', 'marital', 'EC1_1',
                   'D_1_1', 'limit', 'modality', 'w_change',
                   'HE_HBP', 'HE_DB', 'HE_DYSL',
                   'dr_freq', 'dr_amount', 'sm_presnt', 'BP1']
    col_target = ['id', 'Depression', 'MDD']
    
    # column 추출
    df_year = df[col_year]
    df_feature = df[col_feature]
    df_target = df[col_target]
    
    # 분리한 DataFrame들을 Tuple로 출력
    return df_year, df_feature, df_target