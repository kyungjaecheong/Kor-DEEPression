# 라이브러리 및 모듈함수 불러오기
from flask import Flask, render_template, request
import json
from modules_for_app import *

# Flask app 지정
app = Flask(__name__)

# 404 error handling (주소값을 잘 못 입력한 경우)
@app.errorhandler(404)
def page_not_found(error):
    # templates/404.html 실행(404)
    return render_template('404.html'), 404

# home page 실행함수(GET)
@app.route('/', methods=['GET'])
def home():
    # GET request
    if request.method == 'GET':
        # templates/home.html 실행(200)
        return render_template('home.html'), 200

# prediction page 실행함수(GET, POST)
@app.route('/prediction', methods=['GET','POST'])
def prediction():
    # GET request
    if request.method == 'GET':
        # templates/prediction.html 실행(200)
        return render_template('prediction.html'), 200
    
    # POST request(submit으로부터 실행)
    if request.method == 'POST':
        try:
            # Request Form 으로부터 변수를 가져오는 과정부터 실시함
            names_request = list()  # 변수 이름을 담을 리스트
            dict_request = dict()   # 변수 값을 담을 딕셔너리
            
            # 수치형 변수 (Q18 ~ 19, 총 3개) : 변수별로 dtype이 다르기 때문에 따로 진행
            names_numeric = ['age', 'height', 'weight']
            dict_numeric = dict()   # 변수 값을 담을 딕셔너리
            # Q18. Age : integer (19 ~ 80)
            dict_numeric[names_numeric[0]] = int(request.form[names_numeric[0]])
            # Q19. Height : float (100 ~ 200)
            dict_numeric[names_numeric[1]] = float(request.form[names_numeric[1]])
            # Q19. Weight : float (30 ~ 150)
            dict_numeric[names_numeric[2]] = float(request.form[names_numeric[2]])
            # 전체리스트 및 딕셔너리 업데이트
            names_request.extend(names_numeric)
            dict_request.update(dict_numeric)
            
            # 이진형 변수 (Q7 ~ Q13, 7개) : 모두 integer이기 for문으로 진행
            names_binary = ['limitation', 'modality', 'w_change', 'w_control',
                            'high_bp', 'diabetes', 'high_lipid']
            dict_binary = dict()    # 변수 값을 담을 딕셔너리
            # Q 7 ~ 13. 이진형 변수
            for name in names_binary:
                dict_binary[name] = int(request.form[name])
            # 전체리스트 및 딕셔너리 업데이트
            names_request.extend(names_binary)
            dict_request.update(dict_binary)
            
            # 범주형 변수 (Q1 ~ Q6 & Q14 ~ Q17, 총 10개)
            names_category = ['gender','edu','household','marital','economy','health',
                              'drk_freq','drk_amount','smoke','stress']
            dict_category = dict()  # 변수 값을 담을 딕셔너리
            # Q1 ~ Q6 & Q14 ~ Q17. 범주형 변수
            for name in names_category:
                dict_category[name] = int(request.form[name])
            # 전체리스트 및 딕셔너리 업데이트
            names_request.extend(names_category)
            dict_request.update(dict_category)
            
            # (Modeling용 데이터 생성)
            # 수집한 변수 값들을 List로 묶어주기(수치형, 이진형, 범주형 순서)
            values_numeric = [dict_numeric[name] for name in names_numeric]
            values_binary = [dict_binary[name] for name in names_binary]
            values_category = [dict_category[name] for name in names_category]
            # Feature 조합 및 Encoding 실시
            values_encoded_numeric = Encoding_for_model(values_numeric, mode='numeric')
            values_encoded_binary = Encoding_for_model(values_binary, mode='binary')
            values_encoded_category = Encoding_for_model(values_category, mode='category')
            # 리스트 병합 (Global 변수로 지정하여 다른 함수에서 사용할 수 있도록 함)
            global values_encoded
            values_encoded = values_encoded_numeric + values_encoded_binary + values_encoded_category
            
            # (입력 Check용 데이터 생성)
            # 전체 변수이름과 변수값을 묶어서 딕셔너리 정의하기
            values_request = [dict_request[name] for name in names_request]
            dict_values = dict(zip(names_request, values_request))
            
            # 이진형과 범주형은 Label이 따로 존재하므로 이를 정리한 JSON파일로 리스트 생성
            names_bin_cat = names_binary + names_category
            # JSON file 불러오기
            with open('./form_labels.json', 'r', encoding='utf-8') as jf:
                json_reader = json.load(jf)
            # 이진형과 범주형 Label 리스트 생성
            labels_bin_cat = list()
            for name in names_bin_cat:
                label = json_reader[name][f"{dict_values[name]}"]
                labels_bin_cat.append(label)
            
            # 수치형 변수값 리스트를 Label값을 담은 리스트와 병합하여 Check용 딕셔너리 생성
            check_request = values_numeric + labels_bin_cat
            dict_check = dict(zip(names_request, check_request))
            
            # 오류없이 입력이 된 경우 : templates/prediction.html에 리스트 전달(200)
            return render_template('prediction.html', checklist=dict_check), 200
        
        # try문에서 에러가 발생한 경우 : templates/404-2.html 실행(404)
        except:
            return render_template('404-2.html'), 404

# Depression 예측 실행 함수(POST)
@app.route('/result', methods=['POST'])
def result():
    # POST request(submit으로부터 실행)
    if request.method == 'POST':
        pred_mode = request.form['predict_type']
        if pred_mode == 'depr':
            try:
                # model file directory 지정
                depr_dir = './tuning-models/CNN_depr.h5'
                
                # global 변수에 저장한 인코딩된 변수리스트를 불러옴
                list_encoded = values_encoded
                
                # 우울증 예측 (정상vs우울증) : 확률값은 재사용을 위해 global 변수에 저장
                global percent_depr
                prob_depr, pred_depr = model_pred_prob(depr_dir, data=list_encoded)
                # 확률값을 소수점 둘째자리까지 퍼센트로 변환
                percent_depr = int(round(prob_depr, 4)*(10**4))/100
                
                # 오류없이 학습이 진행된 경우 : templates/result.html 실행(200)
                return render_template('result.html', pred_depr=pred_depr, prob_depr=percent_depr), 200
            # try문에서 에러가 발생한 경우 : templates/404-2.html 실행(404)
            except:
                return render_template('404-2.html'), 404
        if pred_mode == 'mdd':
            try:
                # model file directory 지정
                mdd_dir = './tuning-models/MLP_mdd.h5'
                
                # global 변수에 저장한 변수들을 불러옴
                list_encoded = values_encoded
                proba_depr = percent_depr
                
                # 주요우울장애 예측 (경도우울증vs주요우울장애) : 재사용하지 않기 때문에 global저장은 안함
                prob_mdd, pred_mdd = model_pred_prob(mdd_dir, data=list_encoded)
                # 확률값을 소수점 둘째자리까지 퍼센트로 변환
                percent_mdd = int(round(prob_mdd, 4)*(10**4))/100
                
                # 예측한 클래스를 문자열로 이용하기 위해 변환함
                mdd_class = str()
                if pred_mdd == 0:
                    mdd_class = "경도우울증"
                elif pred_mdd == 1:
                    mdd_class = "주요우울장애"
                
                # 오류없이 학습이 진행된 경우 : templates/result.html 실행(200)
                return render_template('result.html',
                                       pred_depr=None, prob_depr=proba_depr,
                                       mdd_class=mdd_class, prob_mdd=percent_mdd), 200
                
            # try문에서 에러가 발생한 경우 : templates/404-2.html 실행(404)
            except:
                return render_template('404-2.html'), 404

# dashboard page 실행함수(GET)
@app.route('/dashboard', methods=['GET'])
def dashboard():
    # GET request
    if request.method == 'GET':
        # templates/dashboard.html 실행(200)
        return render_template('dashboard.html'), 200

# 프로그램 information page 실행함수(GET)
@app.route('/info', methods=['GET'])
def information():
    # GET request
    if request.method == 'GET':
        # templates/info.html 실행(200)
        return render_template('info.html'), 200

# 개발자 정보 page 실행함수(GET)
@app.route('/contact', methods=['GET'])
def contact():
    # GET request
    if request.method == 'GET':
        # templates/info.html 실행(200)
        return render_template('contact.html'), 200

# app.py파일 실행시 실행시킬 함수 : app
if __name__ == '__main__':
    app.run(debug=True)