import os
# from sklearn.preprocessing import StandardScaler
import joblib

# from tensorflow import keras
from keras.models import load_model  
import numpy as np

dl_model_path = os.path.join(os.path.dirname(__file__), 'dl_best_model.h5')
scaler_path = os.path.join(os.path.dirname(__file__), 'scaler_obj.joblib')

model = load_model(dl_model_path)
scaler = joblib.load(scaler_path)


from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def predict(request):
    return render(request, 'predict.html')

def prediction(request):
    if request.method == "POST":
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')
        cp = request.POST.get('chest-pain-type')
        bp = int(request.POST.get('bp'))
        cholestoral = int(request.POST.get('cholestoral'))
        blood_sugar = int(request.POST.get('blood-sugar'))
        electro_result = request.POST.get('electrocardiographic')
        max_heart_rate = int(request.POST.get('heart-rate'))
        exercise_angina = request.POST.get('exercise-induced-angina')
        oldpeak = float(request.POST.get('oldpeak'))
        slope = request.POST.get('slope')

        if gender == "Male":
            gender = 1
        else:
            gender = 0

        if cp == "Typical Angina":
            cp = 0
        elif cp == "Atypical Angina":
            cp = 1
        elif cp == "Non-Anginal Pain":
            cp = 2
        else:
            cp = 3

        if blood_sugar > 120:
            blood_sugar = 1
        else:
            blood_sugar = 0

        if electro_result == "Normal":
            electro_result = 0
        elif electro_result == "Having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)":
            electro_result = 1
        else:
            electro_result = 2

        if exercise_angina == "No":
            exercise_angina = 0
        else:
            exercise_angina = 1

        if slope == "Up-Sloping":
            slope = 0
        elif slope == "Flat":
            slope = 1
        else:
            slope = 2


        input_data = [[age, gender, cp, bp, cholestoral, blood_sugar, electro_result, max_heart_rate, exercise_angina, oldpeak, slope]]
        input_data_scaled = scaler.transform(input_data)

        predicted_value = model.predict(input_data_scaled)
        print('predicted value: ',predicted_value)
        prediction = np.round(model.predict(input_data_scaled)).astype(int)
        if prediction == 1:
            print("yes")
            return JsonResponse({'prediction': 'Yes'})
        else:
            print("no")
            return JsonResponse({'prediction': 'No'})
    
    return render(request, 'predict.html')
