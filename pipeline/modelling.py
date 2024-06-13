from pycaret.regression import *
import logging
import pandas as pd
from pipeline.preprocessing import preprocess_data

def modelling():
    df = pd.read_csv('data/car_data.csv')
    df_clean = preprocess_data(df)
    s = setup(df_clean, target = 'harga', session_id=42)
    best = compare_models()

    # functional API
    save_model(best, 'model/best_modelle')
if __name__ == "__main__":
    modelling()