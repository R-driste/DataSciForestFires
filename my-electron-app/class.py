import joblib
import pandas as pd
import sys
import json
from playsound import playsound

model = joblib.load('heavy_zip/classification/classifymodelfinal.joblib')
try:
    preprocessor = joblib.load('heavy_zip/classification/preprocessor.joblib')
except FileNotFoundError:
    print("Error: preprocessor.joblib not found.", file=sys.stderr)
    sys.exit(1)
try:
    feature_columns = joblib.load('heavy_zip/classification/feature_cols.joblib')
except FileNotFoundError:
    print("Error: feature_cols.joblib not found.", file=sys.stderr)
    sys.exit(1)

raw_input_data_dict = json.load(sys.stdin)

df_raw_input = pd.DataFrame([raw_input_data_dict])
X_processed_array = preprocessor.transform(df_raw_input)
processed_feature_names = preprocessor.get_feature_names_out()
X_processed_df = pd.DataFrame(X_processed_array, columns=processed_feature_names, index=df_raw_input.index)
X_input_final_for_model = X_processed_df.reindex(columns=feature_columns, fill_value=0)

pred = model.predict(X_input_final_for_model)
    
output = {'prediction': pred[0].tolist() if hasattr(pred[0], 'tolist') else pred[0]}

print(json.dumps(output), flush=True)
playsound('tada-fanfare-a-6313.mp3')
