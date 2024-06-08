from flask import Flask, render_template, url_for, jsonify, request
import pickle
from sklearn.ensemble import ExtraTreesRegressor
import pandas as pd
from pycaret.regression import load_model, predict_model

# Inisialisasi Flask

app = Flask(__name__)

# Load model
model = load_model('my_best_pipeline')

@app.route("/")
def beranda():
    return render_template('index.html')

# Definisikan rute untuk melakukan prediksi
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        data = {
            'brand': request.form['brand'],
            'jenis_mobil': request.form['jenis_mobil'],
            'tahun_kendaraan': int(request.form['tahun_kendaraan']),
            'warna': request.form['warna'],
            'transmisi': request.form['transmisi'],
            'kilometer': int(request.form['kilometer']),
            'mesin_enginecc': int(request.form['mesin_enginecc']),
            'bahan_bakar': request.form['bahan_bakar'],
            'dirakit': request.form['dirakit'],
            'penumpang': int(request.form['penumpang']),
            'pintu': int(request.form['pintu'])
        }
        
        df = pd.DataFrame([data])
        
        # Predict car price
        prediction = predict_model(model, data=df)
        predicted_price = prediction['prediction_label'][0]

    # Format hasil prediksi ke dalam format rupiah
    formatted_result = f"Rp{predicted_price:,.0f}".replace(",", ".")

    # Render halaman hasil dengan prediksi
    return render_template('index.html', prediction=formatted_result)


