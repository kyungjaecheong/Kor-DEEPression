'''
Custom Modules for Step 3 Deployment

Project (Step) : Kor-Deepression (Step 3 : Deployment)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

# 함수 리스트 및 __all__ 정의(import * 할 때 불러올 함수들을 정의)
# from custom_modules.postgresql_down import *
__all__ = ['Encoding_for_model',
           #'model_loads',
           #'pred_prob',
           'model_pred_prob']


# 라이브러리 import
import numpy as np
from keras.models import load_model
import tensorflow as tf

# tensorflow-cpu 경고문 출력 없애기
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# Model용 데이터를 얻는 함수(Feature Engineering)
def Encoding_for_model(list_request, mode):
    '''
    Encoding_for_model
        변수들을 조합하여 모델링에 필요한 변수들을 만들어내는 과정
    ---
    입력 변수 정보
        list_request : (List) 변수를 담은 리스트
        mode : (str) "numeric", "binary", "category"
            mode="numeric" : BMI계산, min_max_scaling 실시
            mode="binary" : 체중변화 변수와 체중조절 변수를 하나의 변수로 조합
            mode="category" : One_Hot_Encoding
    ---
    출력 : list
    '''
    # 수치형변수 (age, height, weight) --> (age, BMI)
    if mode == "numeric":
        # 변수리스트를 튜플로 변환하여 함수에서 쓸 변수들을 바로 저장
        age, height, weight = tuple(list_request)
        
        # BMI 연산(몸무게(kg)를 키(m)의 제곱으로 나눔)
        bmi = weight / (height*0.01)**2
        # BMI 이상치를 제한함(modeling과정에서 최소값을 14, 최대값을 50으로 정의했었음)
        if bmi < 14:
            BMI = 14
        elif bmi > 50:
            BMI = 50
        else:
            BMI = bmi
        
        # Min max scaling
            # age 최소값, 최대값 : 19, 80
            # BMI 최소값, 최대값 : 14, 50
        scaled_age = (age - 19) / (80 - 19)
        scaled_bmi = (BMI - 14) / (50 - 14)
        
        # Encoding 완료된 리스트를 반환
        return [scaled_age, scaled_bmi]
    
    # 이진형변수 (총 7개) --> (총 6개)
    elif mode == "binary":
        # 변수리스트를 튜플로 변환하여 함수에서 쓸 변수들을 바로 저장
        limitation, modality, w_change, w_control, high_bp, diabetes, high_lipid = tuple(list_request)
        
        # 체중변화 변수와 체중조절 변수를 하나의 변수로 조합
        if w_change == 1 and w_control == 0:
            # 체중 조절 노력 없이(0) 체중이 변화한 경우(1) --> 1(True)
            w_ch_no_con = 1
        else:
            # 나머지 경우 --> 0(False)
            w_ch_no_con = 0
        
        # Encoding을 따로 거칠 필요는 없어서 최종 리스트를 바로 반환
        return [limitation, modality, w_ch_no_con, high_bp, diabetes, high_lipid]
    
    # 범주형변수 (One_Hot_Encoding)
    elif mode == "category":
        # 변수리스트를 튜플로 변환하여 함수에서 쓸 변수들을 바로 저장
        gender, education, household, marital, economy, health,\
        drink_freq, drink_amount, smoking, stress = tuple(list_request)
        
        # Q 1. Gender [1,2]
        # 초기값을 0으로 설정
        gender_1, gender_2 = 0, 0
        # OneHotEncoding
        if gender == 1:
            gender_1 = 1
        elif gender == 2:
            gender_2 = 1
        # list로 묶어주기
        ohe_gender = [gender_1, gender_2]
        
        # Q 2. Education [1,2,3,4]
        # 초기값을 0으로 설정
        edu_1, edu_2, edu_3, edu_4 = 0, 0, 0, 0
        # OneHotEncoding
        if education == 1:
            edu_1 = 1
        elif education == 2:
            edu_2 = 1
        elif education == 3:
            edu_3 = 1
        elif education == 4:
            edu_4 = 1
        # list로 묶어주기
        ohe_edu = [edu_1, edu_2, edu_3, edu_4]
        
        # Q 3. Household [0,1,2,3]
        # 초기값을 0으로 설정
        house_0, house_1, house_2, house_3 = 0, 0, 0, 0
        # OneHotEncoding
        if household == 0:
            house_0 = 1
        elif household == 1:
            house_1 = 1
        elif household == 2:
            house_2 = 1
        elif household == 3:
            house_3 = 1
        # list로 묶어주기
        ohe_house = [house_0, house_1, house_2, house_3]
        
        # Q 4. Marital status [1,2,3]
        # 초기값을 0으로 설정
        mari_1, mari_2, mari_3 = 0, 0, 0
        # OneHotEncoding
        if marital == 1:
            mari_1 = 1
        elif marital == 2:
            mari_2 = 1
        elif marital == 3:
            mari_3 = 1
        # list로 묶어주기
        ohe_mari = [mari_1, mari_2, mari_3]
        
        # Q 5. Employment [1,2]
        # 초기값을 0으로 설정
        economy_1, economy_2 = 0, 0
        # OneHotEncoding
        if economy == 1:
            economy_1 = 1
        elif economy == 2:
            economy_2 = 1
        # list로 묶어주기
        ohe_economy = [economy_1, economy_2]
        
        # Q 6. Subjective Health [1,2,3,4,5]
        # 초기값을 0으로 설정
        health_1, health_2, health_3, health_4, health_5 = 0, 0, 0, 0, 0
        # OneHotEncoding
        if health == 1:
            health_1 = 1
        elif health == 2:
            health_2 = 1
        elif health == 3:
            health_3 = 1
        elif health == 4:
            health_4 = 1
        # list로 묶어주기
        ohe_health = [health_1, health_2, health_3, health_4, health_5]
        
        # Q14. Drink Frequency [0,1,2,3,4,5,6]
        # 초기값을 0으로 설정
        freq_0, freq_1, freq_2, freq_3, freq_4, freq_5, freq_6 = 0, 0, 0, 0, 0, 0, 0
        # OneHotEncoding
        if drink_freq == 0:
            freq_0 = 1
        elif drink_freq == 1:
            freq_1 = 1
        elif drink_freq == 2:
            freq_2 = 1
        elif drink_freq == 3:
            freq_3 = 1
        elif drink_freq == 4:
            freq_4 = 1
        elif drink_freq == 5:
            freq_5 = 1
        elif drink_freq == 6:
            freq_6 = 1
        # list로 묶어주기
        ohe_freq = [freq_0, freq_1, freq_2, freq_3, freq_4, freq_5, freq_6]
        
        # Q15. Drink Amount [0,1,2,3,4,5]
        # 초기값을 0으로 설정
        amount_0, amount_1, amount_2, amount_3, amount_4, amount_5 = 0, 0, 0, 0, 0, 0
        # OneHotEncoding
        if drink_amount == 0:
            amount_0 = 1
        elif drink_amount == 1:
            amount_1 = 1
        elif drink_amount == 2:
            amount_2 = 1
        elif drink_amount == 3:
            amount_3 = 1
        elif drink_amount == 4:
            amount_4 = 1
        elif drink_amount == 5:
            amount_5 = 1
        # list로 묶어주기
        ohe_amount = [amount_0, amount_1, amount_2, amount_3, amount_4, amount_5]
        
        # Q16. Smoking [0,1]
        # 초기값을 0으로 설정
        smoking_0, smoking_1 = 0, 0
        # OneHotEncoding
        if smoking == 0:
            smoking_0 = 1
        elif smoking == 1:
            smoking_1 = 1
        # list로 묶어주기
        ohe_smoking = [smoking_0, smoking_1]
        
        # Q17. Stress Cognition [4,3,2,1]
        # 초기값을 0으로 설정
        stress_1, stress_2, stress_3, stress_4 = 0, 0, 0, 0
        # OneHotEncoding
        if stress == 1:
            stress_1 = 1
        elif stress == 2:
            stress_2 = 1
        elif stress == 3:
            stress_3 = 1
        elif stress == 4:
            stress_4 = 1
        # list로 묶어주기
        ohe_stress = [stress_1, stress_2, stress_3, stress_4]
        
        # OneHotEncoding으로 묶었던 리스트들을 합치기
        ohe_list = ohe_gender + ohe_edu + ohe_house + ohe_mari + ohe_economy + ohe_health\
            + ohe_freq + ohe_amount + ohe_smoking + ohe_stress
        
        # Encoding 완료된 리스트를 반환
        return ohe_list


# --- 모델과 예측기능으로 나누어 진행했었지만, 조건에따라 메모리가 초과되어버리는 문제 발생

# # 모델 불러오기 기능
# def model_loads(filedir_depr, filedir_mdd):
#     '''
#     model_loads
#         keras 모델 불러오기 기능
#     ---
#     입력 변수 정보
#         filedir : (str)불러올 파일의 디렉토리
#     ---
#     출력 : tuple(keras model objects)
#     '''
#     # Depression(정상vs우울) h5모델 불러오기
#     model_depr = load_model(filedir_depr)
#     # MDD(경도우울vs주요우울) h5모델 불러오기
#     model_mdd = load_model(filedir_mdd)
    
#     # model을 tuple형태로 반환    
#     return model_depr, model_mdd


# # 예측모델 예측실행 기능
# def pred_prob(model, data):
#     '''
#     pred_prob
#         모델을 통해 예측을 실행하는 함수, probability와 predict class를 반환
#     ---
#     입력 변수 정보
#         model : (Keras Object) keras 모델
#         data : (List)  
#     ---
#     출력 : 
#         probability : float (0 ~ 1)
#         predict class : int (0 , 1)
#     '''
#     # Data(list)를 array로 변환
#     array = np.array(data).reshape(1,-1)
    
#     # Predict to Probability (확률값)
#     predict_prob = model.predict(array, verbose=0)[0][0]
    
#     # Probability to Predict class (threshold = 0.5)
#     if predict_prob => 0.5:
#         pred = 0
#     elif predict_prob < 0.5:
#         pred = 1
    
#     # 확률 값을 웹페이지에서 출력하기 위해 퍼센트값으로 변환
#     prob = int(round(predict_prob, 2)*100)
    
#     # 예측 클래스와 확률값을 반환
#     return pred, prob


# 조건에 따라 메모리 초과현상이 발견되어 메모리를 적게 쓰는 방법으로 재구성
    # with문을 통해 예측 진행 후 CPU 메모리 사용을 종료시키도록 함
def model_pred_prob(model_dir, data):
    '''
    model_pred_prob
        모델 불러오기 및 예측기능
    ---
    입력 변수 정보
        model_dir : (str) 불러올 모델의 디렉토리
        data : (list) 예측을 위한 데이터 리스트
    ---
    출력 변수
        probability : float (0 ~ 1)
        predict class : int (0 , 1)
    '''
    # Data(list)를 ndarray로 변환하여 입력
    array = np.array(data).reshape(1, -1)
    
    # with문으로 예측 이후 동작을 멈추게 해본다
    with tf.device("/device:CPU:0"):
        # 모델 불러오기
        model = load_model(model_dir)
        
        # 예측 --> 확률값을 산출
        pred_prob = model.predict(array, verbose=0)
        # 확률 값만 뽑아내어 저장
        prob = pred_prob[0][0]
        
        # 확률값 --> 예측 클래스를 산출 (Threshold=0.5)
        pred_class = np.where(pred_prob<0.5, 0, 1)
        # 예측 클래스 값만 뽑아내어 저장
        pred = pred_class[0][0]
    
    # 불필요한 Retracing방지를 위해 필요없는 변수들은 전부 삭제
    del array
    del model
    del pred_prob
    del pred_class
    
    # 확률값과 예측클래스를 최종적으로 출력함
    return prob, pred


# ---테스트용 코드---
# test_list = [0.5,0.5,1]+[0 for _ in range(44)]

# list를 ndarray가 아닌 tensor형태로 바꾸어 본다
    # 메모리 초과 발생 ... array로 실행
# # test_tensor = tf.convert_to_tensor(test_list)
# # test_tensor_reshape = tf.reshape(test_tensor,shape=[1,47])

# test_dir = './tuning-models/CNN_depr.h5'
# # with tf.device("/device:CPU:0"):
# #     model = load_model(test_dir)
# #     test_prob = model.predict(test_tensor_reshape)
# # print(test_prob)

# test_prob, test_class = model_pred_prob(test_dir, test_list)
# print(test_prob, test_class)

# import json
# with open('./form_labels.json', 'r', encoding='utf-8') as jf:
#     json_reader = json.load(jf)
# test_gender = 1
# print(json_reader["gender"][f"{test_gender}"])