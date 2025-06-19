import joblib
import pandas as pd
import sys
import json
from playsound import playsound

def main():
    model = joblib.load('classifymodelfinal.joblib')

    try:
        preprocessor = joblib.load('preprocessor.joblib')
    except FileNotFoundError:
        print("Error: preprocessor.joblib not found. Make sure it's saved in the correct path.", file=sys.stderr)
        sys.exit(1)

    try:
        feature_columns = joblib.load('feature_cols.joblib')
    except FileNotFoundError:
        print("Error: feature_columns.joblib not found. Make sure it's saved in the correct path.", file=sys.stderr)
        sys.exit(1)

    input_str = sys.argv[1]
    input_data = json.loads(input_str)

    with open("in.txt", 'a') as f: # 'a' for append mode
            f.write(input_str + '\n\n')
    
    df_raw_input = pd.DataFrame([input_data])
    X_processed_array = preprocessor.transform(input_data)
    processed_feature_names = preprocessor.get_feature_names_out()
    X_processed_df = pd.DataFrame(X_processed_array, columns=processed_feature_names, index=df_raw_input.index)
    X_processed_df.to_json("aprocessed_input_for_model.json", orient="records", lines=True)

    pred = model.predict(X_processed_df)
    output = {'prediction': pred[0].tolist() if hasattr(pred[0], 'tolist') else pred[0]}
    print(json.dumps(output), flush=True)
    with open("afinaljson.json", 'w') as f:
        json.dump(output, f, indent=4)

    with open("out.txt", 'a') as f: # 'a' for append mode
            f.write(input_str + '\n\n')
    playsound('tada-fanfare-a-6313.mp3')

if __name__ == '__main__':
    main()
