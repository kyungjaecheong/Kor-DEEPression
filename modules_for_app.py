'''
Custom Modules for Step 3 Deployment

Project (Step) : Kor-Deepression (Step 3 : Deployment)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''

# 함수 리스트 및 __all__ 정의(import * 할 때 불러올 함수들을 정의)
# from custom_modules.postgresql_down import *
# __all__ = ['Encoding_for_model']

# 라이브러리 import
import os
import json
import numpy as np
from tensorflow import lite as tflite

# tensorflow-cpu 경고문 출력 없애기
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
    
    # 범주형변수 (One_Hot_Encoding) (총 10개) --> (총 39개)
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
        
        # OneHotEncoding으로 묶었던 리스트들을 하나의 리스트로 합치기
        ohe_list = ohe_gender + ohe_edu + ohe_house + ohe_mari + ohe_economy + ohe_health\
            + ohe_freq + ohe_amount + ohe_smoking + ohe_stress
        
        # Encoding 완료된 리스트를 반환
        return ohe_list


# Check용 데이터를 얻는 함수(from JSON)
def Decoding_for_check(json_dir, dict_request, names_list):
    '''
    Decoding_for_check
        숫자로 인코딩 값들을 따로 작성한 JSON문서에 기반하여 문자열로 바꾸어주는 기능 
    ---
    입력 변수 정보
        json_dir : (str) JSON 파일의 directory
        dict_request : (Dict) 변수이름과 값을 담은 딕셔너리
        names_list : (List) 변수이름들을 순서대로 담은 리스트
    ---
    출력 : List
    '''
    # JSON 파일 불러오기
    with open(json_dir, 'r', encoding='utf-8') as jf:
        json_reader = json.load(jf)
    
    # Label list를 담을 빈 리스트를 정의
    labels_list = list()
    
    # for문으로 names_list 순서대로 레이블값을 append
    for name in names_list:
        label = json_reader[name][f"{dict_request[name]}"]
        labels_list.append(label)
    
    # Label로 Decoding한 리스트를 최종적으로 출력함
    return labels_list


# 모델 예측 기능 (tensorflow-lite)
    # 경량화 없이 1차 개발을 완료했으나, Koyeb free-tier(nano)의 한계로 오류가 자주 발생함
    # Keras 모델(.h5)로 predict를 실행하는 것이 생각보다 리소스를 많이 잡아먹는 작업임을 깨달음
    # 따라서 이를 개선하기 위해 Keras모델을 tensorflow-lite를 통해 경량화하여 진행해보았음
        # 이에 대한 코드는 final-models 폴더에 저장되어 있음
    # 테스트 결과 압도적인 속도의 개선을 확인했으며, 그동안 발생했었던 오류와 경고들도 더 이상 발생하지 않음을 확인함
def predict_prob_tflite(data, model_dir):
    '''
    predict_prob_tflite
        tensorflow-lite를 이용하여 예측 확률값을 얻는 기능 
    ---
    입력 변수 정보
        data : (list) 예측하고자하는 데이터
        model_dir : (str) tflite model의 directory
    ---
    출력 변수
        prob : (float) 예측 확률값의 퍼센트값 (소수점 둘째자리)
        pred : (int) 예측 클래스 (0 or 1)
    '''
    # 모델 불러오기
    interpreter = tflite.Interpreter(model_path=model_dir)
    # 메모리 할당하기
    interpreter.allocate_tensors()
    # input, output 정보담기
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # data를 input shape에 맞게 변경
    input_shape = input_details[0]['shape']
    input_data = np.array(data, dtype=np.float32).reshape(input_shape)
    
    # tensor에 맞게 세팅 후 invoke실시
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    # 예측 실행 (확률값이 출력됨)
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # 출력변수1) 예측 확률값을 퍼센트로 변환
    prob = int(round(output_data[0][0], 4)*(10**4))/100
    
    # 출력변수2) 확률 값을 통해 예측 클래스를 반환 (기준은 0.5)
    pred = np.where(output_data<0.5, 0, 1)[0][0]
    
    # 출력변수들 최종 반환
    return prob, pred