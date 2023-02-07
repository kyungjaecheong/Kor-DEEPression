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
        # Request Form 으로부터 변수 얻어내는 과정부터 실시함
            
            # 범주형_1 (Gender ~ Subjective Health) (Q1 ~ Q6, 6개)
            # Q 1. Gender [1,2]
            gender = int(request.form['gender'])
            # Q 2. Education [1,2,3,4]
            education = int(request.form['edu'])            
            # Q 3. Household [0,1,2,3]
            household = int(request.form['household'])
            # Q 4. Marital status [1,2,3]
            marital = int(request.form['marital'])
            # Q 5. Employment [1,2]
            economy = int(request.form['economy'])
            # Q 6. Subjective Health [1,2,3,4,5]
            health = int(request.form['health'])
            
            # 이진형 (Limitation ~ Dyslipidemia) (Q7 ~ Q13, 7개)
            # Q 7. Limitation [0,1]
            limitation = int(request.form['limitation'])
            # Q 8. Modality [0,1]
            modality = int(request.form['modality'])
            # Q 9. Weight Change [0,1]
            w_change = int(request.form['w_change'])
            # Q10. Weight Control [0,1]
            w_control = int(request.form['w_control'])
            # Q11. Hypertension [0,1]
            high_bp = int(request.form['high_bp'])
            # Q12. Diabetes [0,1]
            diabetes = int(request.form['diabetes'])
            # Q13. Dyslipidemia [0,1]
            high_lipid = int(request.form['high_lipid'])
            
            # 범주형_2 (Drink Frequency ~ Stress) (Q14 ~ Q17, 4개)
            # Q14. Drink Frequency [0,1,2,3,4,5,6]
            drink_freq = int(request.form['drk_freq'])
            # Q15. Drink Amount [0,1,2,3,4,5]
            drink_amount = int(request.form['drk_amount'])
            # Q16. Smoking [0,1]
            smoking = int(request.form['smoke'])
            # Q17. Stress Cognition [4,3,2,1]
            stress = int(request.form['stress'])
            
            # 수치형 (Age, Height, Weight) (Q18 ~ 19, 3개)
            # Q18. Age : integer (19 ~ 80)
            age = int(request.form['age'])
            # Q19. Height : float (100 ~ 200)
            height = float(request.form['height'])
            # Weight : float (30 ~ 150)
            weight = float(request.form['weight'])
            
            # 수집한 변수들을 List로 묶어주기(수치형, 이진형, 범주형 순서)
            list_numeric = [age, height, weight]
            list_binary = [limitation, modality, w_change, w_control, high_bp, diabetes, high_lipid]
            list_category = [gender, education, household, marital, economy, health,
                             drink_freq, drink_amount, smoking, stress]
            
            # Feature 조합 및 Encoding 실시
            list_encoded_numeric = Encoding_for_model(list_numeric, mode='numeric')
            list_encoded_binary = Encoding_for_model(list_binary, mode='binary')
            list_encoded_category = Encoding_for_model(list_category, mode='category')
            # 리스트 병합
            list_encoded = list_encoded_numeric + list_encoded_binary + list_encoded_category
            
            # 최종 Model들 불러오기
            dir_depr = './tuning-models/CNN_depr.h5'
            dir_mdd = './tuning-models/MLP_mdd.h5'
            # model_depr, model_mdd = model_loads(dir_depr, dir_mdd)
            
            # 우울증 예측 (정상vs우울증)
            # pred_depr, prob_depr = pred_prob(model_depr, list_encoded)
            prob_depr, pred_depr = model_pred_prob(dir_depr, list_encoded)
            
            # 우울증이 있는 경우 : 주요우울장애 예측 (경도우울증vs주요우울장애)
            if pred_depr == 1:
                # pred_mdd, prob_mdd = pred_prob(model_mdd, list_encoded)
                prob_mdd, pred_mdd = model_pred_prob(dir_mdd, list_encoded)
            elif pred_depr == 0:
                pred_mdd, prob_mdd = None, None
            
            # 오류없이 templates/result.html 실행(200)
            return render_template('result.html',
                                   pred_depr=pred_depr, prob_depr=prob_depr,
                                   pred_mdd=pred_mdd, prob_mdd=prob_mdd), 200
        except:
            return render_template('404-2.html'), 404

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if request.method == 'GET':
        return render_template('dashboard.html'), 200

@app.route('/info', methods=['GET'])
def information():
    if request.method == 'GET':
        return render_template('info.html'), 200

@app.route('/contact', methods=['GET'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html'), 200

if __name__ == '__main__':
    app.run(debug=True)