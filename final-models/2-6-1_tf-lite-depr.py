'''
Python Code for Step 2-6 Convert Final models to tf-lite

Project (Step) : Kor-Deepression (Step 2 : Modeling)

Project_repo_url : https://github.com/kyungjaecheong/Kor-DEEPression

Contributor : Kyung Jae, Cheong (정경재)
'''
'''
CLI command for running
$ python final-models/2-6-1_tf-lite-depr.py
'''

# 라이브러리 import
import os
import numpy as np
import tensorflow as tf
import keras

# tensorflow-cpu 경고문 출력 없애기
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# .h5 모델 불러오기 (CNN_depr.h5)
model_depr = keras.models.load_model('./tuning-models/CNN_depr.h5')

# model 예측 테스트 (sample중 가장 높은 확률을 나타낸 case로 테스트함)
print("Prediction Test")
test_input = [0.6557377049180327,0.1793442469983833,1,1,1,0,1,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0]
test_array = np.array(test_input).reshape(1,-1)
test_output = model_depr.predict(test_array ,verbose=False)
print("Test output: ", test_output)
'''
Prediction Test
Test output:  [[0.99963725]]
'''

# 모델 구조 시각화 --> png image로 저장
keras.utils.plot_model(model_depr, to_file='./final-models/final_depr_img.png',
                       show_shapes=True, show_layer_names=True,
                       rankdir='TB', expand_nested=False, dpi=96)

# directory 형식으로 저장하는 것을 권장하므로 directory로 모델 저장
model_depr.save('./final-models/model_depr')

# 저장 모델 예측 테스트 (동일한 테스트 데이터로 실시함)
test_load_model_depr = keras.models.load_model('./final-models/model_depr')
test_load_output = test_load_model_depr.predict(test_array ,verbose=False)
print("Test loaded model: ", test_load_output)
'''
Test loaded model:  [[0.99963725]]
'''

# Convert to .tflite format (lite모델 변환)
converter_depr = tf.lite.TFLiteConverter.from_saved_model('./final-models/model_depr')
tflite_depr = converter_depr.convert()
open('./final-models/final_model_depr.tflite','wb').write(tflite_depr)


# Interpretation of .tflite model (lite모델 테스트)

# 불러오기
interpreter_depr = tf.lite.Interpreter(model_path='./final-models/final_model_depr.tflite')

# 할당하기
interpreter_depr.allocate_tensors()

# input, output 정보 저장
input_detail_depr = interpreter_depr.get_input_details()
output_detail_depr = interpreter_depr.get_output_details()

# input shape 형태 확인하기
input_shape_depr = input_detail_depr[0]['shape']
print("Input shape of Model_depr: ", input_shape_depr)
'''
Input shape of Model_depr: [ 1 47  1]
'''

# input shape에 맞게 테스트 데이터(list)를 array로 변환 (dtype은 float32로 맞춰줘야 동작함)
input_test_data = np.array(test_input, dtype=np.float32).reshape(input_shape_depr)
print("Shape of test input : ", input_test_data.shape)
'''
Shape of test input :  (1, 47, 1)
'''

# input data를 tensor에 맞게 세팅 후 모델을 thread에 의해 손상되지 않도록 invoke함수를 실행함
interpreter_depr.set_tensor(input_detail_depr[0]['index'], input_test_data)
interpreter_depr.invoke()

# 예측을 실행하여 동작 확인
output_test_data = interpreter_depr.get_tensor(output_detail_depr[0]['index'])
print("Output of Model_depr: ", output_test_data)
'''
Output of Model_depr:  [[0.9996372]]
'''
