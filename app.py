'''
CLI command for running
$ python app.py
'''

# 라이브러리 및 모듈함수 불러오기
from flask import Flask, render_template, request
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
            
            # 범주형 변수 (Q1 ~ Q6 & Q14 ~ Q17, 총 10개) : 모두 integer이기 for문으로 진행
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
            
            # Feature 조합 및 Encoding 실시 (Custom 모듈에서 따로 정의하여 실행)
            values_encoded_numeric = Encoding_for_model(values_numeric, mode='numeric')
            values_encoded_binary = Encoding_for_model(values_binary, mode='binary')
            values_encoded_category = Encoding_for_model(values_category, mode='category')
            
            # 리스트 병합 (Global 변수로 지정하여 다른 함수에서 사용할 수 있도록 함)
            global values_encoded
            values_encoded = values_encoded_numeric + values_encoded_binary + values_encoded_category
            
            
            # (입력 Check용 데이터 생성)            
            # 이진형과 범주형은 Label이 따로 존재하므로 변수명 리스트를 순서대로 묶기(이진형, 범주형 순서)
            names_bin_cat = names_binary + names_category
            
            # Decoding 실시 (Custom 모듈에서 따로 정의하여 실행)
            labels_bin_cat = Decoding_for_check(json_dir='./form_labels.json',
                                                dict_request=dict_request,
                                                names_list=names_bin_cat)
            
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
                # 모델 directory 지정
                model_depr_path = './final-models/final_model_depr.tflite'
                
                # 우울증 예측 (정상vs우울증)
                global depr_prob    # MDD 예측 결과페이지에서 쓰기위해 global 변수로 저장
                depr_prob, depr_pred = predict_prob_tflite(values_encoded, model_depr_path)
                
                # 오류없이 학습이 진행된 경우 : templates/result.html 실행(200)
                return render_template('result.html', pred_depr=depr_pred, prob_depr=depr_prob), 200
            
            # try문에서 에러가 발생한 경우 : templates/404-2.html 실행(404)
            except:
                return render_template('404-2.html'), 404
        if pred_mode == 'mdd':
            try:
                # 모델 directory 지정
                model_mdd_path = './final-models/final_model_mdd.tflite'
                
                # 주요우울장애 예측 (경도우울증vs주요우울장애)
                mdd_prob, mdd_pred = predict_prob_tflite(values_encoded, model_mdd_path)
                
                # 결과창에서 예측 클래스를 문자열로 출력하기위해 Decoding
                mdd_class = str()
                if mdd_pred == 0:
                    mdd_class = "경도우울증"
                elif mdd_pred == 1:
                    mdd_class = "주요우울장애"
                
                # 오류없이 학습이 진행된 경우 : templates/result.html 실행(200)
                return render_template('result.html',
                                       pred_depr=None, prob_depr=depr_prob,
                                       mdd_class=mdd_class, prob_mdd=mdd_prob), 200
                
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