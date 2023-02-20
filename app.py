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

# 405 error handling (GET/POST 에러가 발생한 경우)
@app.errorhandler(405)
def method_not_allowed(error):
    # templates/405.html 실행(405)
    return render_template('405.html'), 405

# home page 실행함수(GET)
@app.route('/', methods=['GET'])
def home():
    # GET request
    if request.method == 'GET':
        # templates/home.html 실행(200)
        return render_template('home.html'), 200

# prediction page 실행함수(GET, POST)
    # 입력과 예측을 분리하면 여러기기에서 동시에 입력했을 경우에
    # 서로 값이 꼬이는 현상이 발견되어 입력과 예측을 한번에 진행하도록 함
    # 결과 값을 계속해서 다음 페이지에 넘겨주는 방식으로 전달 함 
@app.route('/prediction', methods=['GET','POST'])
def prediction():
    # GET request
    if request.method == 'GET':
        # templates/prediction.html 실행(200)
        return render_template('prediction.html'), 200
    
    # POST request(submit으로부터 실행)
    if request.method == 'POST':
        try:
            '''
            Request Form 으로부터 변수를 가져오기
            '''
            # 전체 변수이름과 값을 담을 리스트와 딕셔너리
            names_request = list()  # 변수 이름을 담을 리스트
            dict_request = dict()   # 변수 이름과 값을 담을 딕셔너리
            
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
            
            # 이진형 변수 (Q7 ~ Q13, 7개) : 모두 integer이기 때문에 for문으로 진행
            names_binary = ['limitation', 'modality', 'w_change', 'w_control',
                            'high_bp', 'diabetes', 'high_lipid']
            dict_binary = dict()    # 변수 값을 담을 딕셔너리
            # Q 7 ~ 13. 이진형 변수
            for name in names_binary:
                dict_binary[name] = int(request.form[name])            
            # 전체리스트 및 딕셔너리 업데이트
            names_request.extend(names_binary)
            dict_request.update(dict_binary)
            
            # 범주형 변수 (Q1 ~ Q6 & Q14 ~ Q17, 총 10개) : 모두 integer이기 때문에 for문으로 진행
            names_category = ['gender','edu','household','marital','economy','health',
                              'drk_freq','drk_amount','smoke','stress']
            dict_category = dict()  # 변수 값을 담을 딕셔너리
            # Q1 ~ Q6 & Q14 ~ Q17. 범주형 변수
            for name in names_category:
                dict_category[name] = int(request.form[name])            
            # 전체리스트 및 딕셔너리 업데이트
            names_request.extend(names_category)
            dict_request.update(dict_category)
            
            
            '''
            Modeling용 데이터 생성
            '''
            # 수집한 변수 값들을 List로 묶어주기(수치형, 이진형, 범주형 순서)
            values_numeric = [dict_numeric[name] for name in names_numeric]
            values_binary = [dict_binary[name] for name in names_binary]
            values_category = [dict_category[name] for name in names_category]
            
            # Feature 조합 및 Encoding 실시 (modules_for_app에서 불러온 함수)
            values_encoded_numeric = Encoding_for_model(values_numeric, mode='numeric')
            values_encoded_binary = Encoding_for_model(values_binary, mode='binary')
            values_encoded_category = Encoding_for_model(values_category, mode='category')
            
            # 리스트 병합
            values_encoded = values_encoded_numeric + values_encoded_binary + values_encoded_category
            
            
            '''
            입력 Check용 데이터 생성
            '''
            # 이진형과 범주형은 Label이 따로 존재하므로 변수명 리스트를 순서대로 묶기(이진형, 범주형 순서)
            names_bin_cat = names_binary + names_category
            
            # Decoding 실시 (modules_for_app에서 불러온 함수)
            labels_bin_cat = Decoding_for_check(json_dir='./form_labels.json',
                                                dict_request=dict_request,
                                                names_list=names_bin_cat)
            
            # 수치형 변수값 리스트를 Label값을 담은 리스트와 병합하여 Check용 딕셔너리 생성
            check_request = values_numeric + labels_bin_cat
            dict_check = dict(zip(names_request, check_request))
            
            
            '''
            우울증 및 주요우울장애 예측
                확률퍼센트값과 예측클래스를 산출
            '''
            # 모델(.tflite)파일 디렉토리 지정
            model_dir_depr = './final-models/final_model_depr.tflite'
            model_dir_mdd = './final-models/final_model_mdd.tflite'
            
            # Depression 모델 예측 (확률 퍼센트값 & 예측 클래스)
            prob_depr, pred_depr = predict_prob_tflite(values_encoded, model_dir_depr)
            
            # 예측 클래스를 문자열로 Decoding
            class_depr = str()
            if pred_depr == 0:
                class_depr = "정상"
            elif pred_depr == 1:
                class_depr = "우울증"
            
            '''
            확인 페이지 출력 (예측 결과도 넘겨주기)
            '''
            # "정상" 인 경우 : 다음 단계로 바로 넘어감
            if class_depr == "정상":
                # templates/prediction.html에 변수들을 전달 (200)
                return render_template('prediction.html',
                                       checklist = dict_check,
                                       percnt_depr = prob_depr,
                                       label_depr = class_depr), 200
            
            # "우울증" 인 경우 : MDD 모델 예측을 추가적으로 실시
            elif class_depr == "우울증":
                # MDD 모델 예측 (확률 퍼센트값 & 예측 클래스)
                prob_mdd, pred_mdd = predict_prob_tflite(values_encoded, model_dir_mdd)

                # 예측 클래스를 문자열로 Decoding
                class_mdd = str()
                if pred_mdd == 0:
                    class_mdd = "경도우울증"
                elif pred_mdd == 1:
                    class_mdd = "주요우울장애"
                
                # 오류없이 예측을 수행한 경우 : templates/prediction.html에 변수들을 전달 (200)
                return render_template('prediction.html',
                                       checklist = dict_check,
                                       percnt_depr = prob_depr,
                                       label_depr = class_depr,
                                       percnt_mdd = prob_mdd,
                                       label_mdd = class_mdd), 200
        
        # try문에서 에러가 발생한 경우 : templates/404-2.html 실행(404)
        except:
            return render_template('404-2.html'), 404

# 예측 결과 출력 함수(POST)
@app.route('/result', methods=['POST'])
def result():
    # POST request(submit으로부터 실행)
    if request.method == 'POST':
        # submit 버튼 값 가져오기
        pred_mode = request.form['predict_type']
        
        # submit 값이 "depr"인경우
        if pred_mode == 'depr':
            try:
                # 변수 가져오기
                depr_prob = request.form['depr_percnt']
                depr_class  = request.form['depr_class']
                
                # "정상"인 경우 : 바로 결과페이지로 이동
                if depr_class == "정상":
                    # templates/result.html 실행(200)
                    return render_template('result.html',
                                           percnt_depr = depr_prob,
                                           label_depr = depr_class), 200
                
                # "우울증"인 경우 : 변수를 추가적으로 가져오고 결과페이지로 이동
                elif depr_class == "우울증":
                    # 변수 가져오기
                    mdd_prob = request.form['mdd_percnt']
                    mdd_class = request.form['mdd_class']
                    
                    # templates/result.html 실행(200)
                    return render_template('result.html',
                                           percnt_depr = depr_prob,
                                           label_depr = depr_class,
                                           percnt_mdd = mdd_prob,
                                           label_mdd = mdd_class), 200
            
            # try문에서 에러가 발생한 경우 : templates/404-2.html 실행(404)
            except:
                return render_template('404-2.html'), 404
        
        # submit 값이 "mdd"인경우
        if pred_mode == 'mdd':
            try:
                # 변수 가져오기
                add_depr_prob = request.form['add_depr_percnt']
                add_depr_class = request.form['add_depr_class']
                add_mdd_prob = request.form['add_mdd_percnt']
                add_mdd_class = request.form['add_mdd_class']
                
                # templates/result.html 실행(200)
                return render_template('result.html',
                                       add_percnt_depr = add_depr_prob,
                                       add_label_depr = add_depr_class,
                                       add_percnt_mdd = add_mdd_prob,
                                       add_label_mdd = add_mdd_class), 200
                
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