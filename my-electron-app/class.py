'''
This python helper script is used to classify the input data for risk assessment.
'''
import joblib
import pandas as pd
import sys
import json
import simpleaudio as sa
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

wave_obj = sa.WaveObject.from_wave_file(os.path.join(BASE_DIR, 'audio', 'clock.wav'))
play_obj = wave_obj.play()
play_obj.wait_done()

#load all necessary model related files
model = joblib.load(os.path.join(BASE_DIR, 'heavy_zip', 'classification', 'classifymodelfinal.joblib'))

try:
    preprocessor = joblib.load(os.path.join(BASE_DIR, 'heavy_zip', 'classification', 'preprocessor.joblib'))
except FileNotFoundError:
    print("Error: preprocessor.joblib not found :(", file=sys.stderr)
    sys.exit(1)
try:
    feature_columns = joblib.load(os.path.join(BASE_DIR, 'heavy_zip', 'classification', 'feature_cols.joblib'))
except FileNotFoundError:
    print("Error: feature_cols.joblib not found :(", file=sys.stderr)
    sys.exit(1)

play_obj = wave_obj.play()
play_obj.wait_done()

#load and feed input data
try:
    raw_input_data_dict = json.load(sys.stdin)
    df_raw_input = pd.DataFrame([raw_input_data_dict])
    X_processed_array = preprocessor.transform(df_raw_input)
    processed_feature_names = preprocessor.get_feature_names_out()
    X_processed_df = pd.DataFrame(X_processed_array, columns=processed_feature_names, index=df_raw_input.index)
    X_input_final_for_model = X_processed_df.reindex(columns=feature_columns, fill_value=0)

    pred = model.predict(X_input_final_for_model) #success hopefully
        
    output = {'prediction': pred[0].tolist() if hasattr(pred[0], 'tolist') else pred[0]}
    wave_obj = sa.WaveObject.from_wave_file(os.path.join(BASE_DIR, 'audio', 'positive.wav'))
    play_obj = wave_obj.play()
    play_obj.wait_done()
    print(json.dumps(output), flush=True)
except Exception as e:
    output = {'prediction': 3, 'error': str(e)} #inputs must have been bad
    wave_obj = sa.WaveObject.from_wave_file(os.path.join(BASE_DIR, 'audio', 'wrong.wav'))
    play_obj = wave_obj.play()
    play_obj.wait_done()
    print(json.dumps(output), flush=True)
