from flask import Flask, render_template, request
import numpy as np
from keras.models import load_model

app = Flask(__name__)

model = load_model("./data/deep_model2.h5")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html'), 200

@app.route('/prediction', methods=['GET','POST'])
def prediction():
    if request.method == 'GET':
        return render_template('prediction.html'), 200
    if request.method == 'POST':
        try:
            gender = int(request.form['gender'])
            age = int(request.form['age'])
            edu = int(request.form['edu'])
            cfam = int(request.form['cfam'])
            marital = int(request.form['marital'])
            health = int(request.form['health'])
            modality = int(request.form['modality'])
            economy = int(request.form['economy'])
            w_change = int(request.form['w_change'])
            w_control = int(request.form['w_control'])
            drink = int(request.form['drink'])
            drink_once = int(request.form['drink_once'])
            stress = int(request.form['stress'])
            smoke = int(request.form['smoke'])
            
            if health in [1,2] or modality == 1:
                h_state = 0
            else:
                h_state = 1
            
            if w_change in [2,3] and w_control == 4:
                weight = 1
            else:
                weight = 0
            
            if drink == 1 and gender == 0 and drink_once == 4:
                drinking = 2
            elif drink == 1 and gender == 1 and drink_once in [3,4]:
                drinking = 2
            elif drink == 0 or drink_once == 0:
                drinking = 0
            else:
                drinking = 1
            
            var_gen = (gender - 0) / (1 - 0)
            var_age = (age - 20) / (80 - 20)
            var_edu = (edu - 0) / (3 - 0)
            var_cfm = (cfam - 1) / (5 - 1)
            var_mar = (marital - 0) / (1 - 0)
            var_hms = (h_state - 0) / (1 - 0)
            var_eco = (economy - 0) / (1 - 0)
            var_wch = (weight - 0) / (1 - 0)
            var_drk = (drinking - 0) / (2 - 0)
            var_sts = (stress - 0) / (3 - 0)
            var_smk = (smoke - 0) / (1 - 0)
            
            array = np.array([[var_gen, var_age, var_edu, var_cfm, var_mar, var_hms, var_eco, var_wch, var_drk, var_sts, var_smk]])
            
            predict_prob = model.predict(array, verbose=0)[0][0]
            
            if predict_prob < 0.5:
                label = 0
            else:
                label = 1
            
            label_dict = {0:'정상(Normal)', 1:'우울증(Depression)'}
            
            pred = label_dict[label]
            prob = int(round(predict_prob, 2)*100)
            
            return render_template('result.html', pred=pred, prob=prob)
        except:
            return render_template('404-2.html')

@app.route('/info', methods=['GET'])
def information():
    if request.method == 'GET':
        return render_template('info.html'), 200

if __name__ == '__main__':
    app.run(debug=True)