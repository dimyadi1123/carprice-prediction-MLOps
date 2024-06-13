from flask import Flask, render_template, url_for, jsonify, request
from flask_cors import CORS
import pickle
from sklearn.ensemble import ExtraTreesRegressor
import pandas as pd
import os
from pycaret.regression import load_model, predict_model
from apscheduler.schedulers.background import BackgroundScheduler
# from pipeline.ingestion import scheduled_scraping_job
from pipeline.modelling import modelling
from apscheduler.triggers.cron import CronTrigger
import atexit


# Inisialisasi Flask

app = Flask(__name__)

# Load model
model = load_model('model/best_modelle')


@app.route("/")
def beranda():
    # Lakukan sesuaikan path dengan struktur direktori kamu
    return render_template('index.html')

# def index():
#     list_mobil = show_list()
#     return render_template('index.html', list_mobil=list_mobil)

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

# def show_list():
#     df_tabel = pd.read_csv('mobil123_fix.csv')
#     nama_mobil = df_tabel['nama_mobil']
#     harga = df_tabel['harga']
    
#     # Buat list of dictionaries
#     mobil_list = []
#     for i in range(len(nama_mobil)):
#         mobil_list.append({
#             'nama_mobil': nama_mobil[i],
#             'harga': harga[i]
#         })
    
# #     return mobil_list
       

# def run_scheduled_tasks():
#     try:
#         # scheduled_scraping_job()
#         modelling()
#     except Exception as e:
#         print(f"Error running scheduled tasks: {e}")

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=run_scheduled_tasks, trigger=CronTrigger(hour=00, minute=00))
# scheduler.start()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

if __name__ == "_main_":
    app.run(debug=True, use_reloader=False)


