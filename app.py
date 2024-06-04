from flask import Flask, render_template, url_for, jsonify, request
import pickle
from sklearn.ensemble import ExtraTreesRegressor
import xgboost as xgb

# Inisialisasi Flask

app = Flask(__name__)

# # Fungsi untuk memuat label encoder dengan penanganan error
# def load_label_encoder(filename):
#     try:
#         with open(filename, 'rb') as file:
#             return pickle.load(file)
#     except FileNotFoundError:
#         print(f"Error: File {filename} not found.")
#     except Exception as e:
#         print(f"Error loading {filename}: {e}")

# # Muat label encoder yang telah disimpan
# le_bahan_bakar = load_label_encoder('le_bahan_bakar.pkl')
# le_brand = load_label_encoder('le_brand.pkl')
# le_dirakit = load_label_encoder('le_dirakit.pkl')
# le_jenis_mobil = load_label_encoder('le_jenis_mobil.pkl')
# le_transmisi = load_label_encoder('le_transmisi.pkl')
# le_warna = load_label_encoder('le_warna.pkl')

@app.route("/")
def beranda():
    return render_template('index.html')

# Definisikan rute untuk melakukan prediksi
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    # Mengambil data dari form dan mengonversi ke tipe data yang sesuai
    tahun = int(request.form.get('tahun'))
    kilometer = float(request.form.get('kilometer'))
    penumpang = int(request.form.get('penumpang'))
    transmisi = int(request.form.get('transmisi'))
    warna = int(request.form.get('warna'))
    mesin_cc = float(request.form.get('mesin_cc'))
    pintu = int(request.form.get('pintu'))
    jenis_mobil = int(request.form.get('jenis_mobil'))
    bahan_bakar = int(request.form.get('bahan_bakar'))
    dirakit = int(request.form.get('dirakit'))
    brand = int(request.form.get('brand'))

    data_for_prediction = [tahun, kilometer, penumpang, transmisi, warna, mesin_cc, pintu, jenis_mobil, bahan_bakar, dirakit, brand]

    # Load model Random Forest
    with open('xgb.pkl', 'rb') as model_file:
        xgb_model = pickle.load(model_file)

    # Lakukan prediksi
    result = xgb_model.predict([data_for_prediction])[0]

    # Format hasil prediksi ke dalam format rupiah
    formatted_result = f"Rp{result:,.0f}".replace(",", ".")

    # Render halaman hasil dengan prediksi
    return render_template('index.html', prediction=formatted_result)

