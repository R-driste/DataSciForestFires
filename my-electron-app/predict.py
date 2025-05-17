import sys
import json
import joblib
import numpy as np

model = joblib.load("/Users/dristiroy/DATASCIFORESTFIRES/DataSciForestFires/my-electron-app/regression_model.pkl")

args = sys.argv
inputs = json.loads(args[1])
selected_feature = args[2]
if selected_feature in inputs:
    del inputs[selected_feature]
input_values = np.array(list(inputs.values())).reshape(1, -1)
prediction = model.predict(input_values)[0]

print(json.dumps(prediction))
print("RAN PREDICT YAY")