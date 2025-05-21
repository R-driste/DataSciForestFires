import sys
import joblib
import json
import pandas as pd

#load model weights
classifier = joblib.load("../models/unzipped_models/classifymodel_2.joblib")
print("MODEL LOADED!")
input_json = sys.stdin.read()
input_data = json.loads(input_json)

list_yay = ['Zip Code', '* CAL FIRE Unit', 'Hazard Type', 
       'Structure Defense Actions Taken', '* Structure Type',
       '# Units in Structure (if multi unit)', 
       '* Roof Construction',
       '* Eaves', '* Vent Screen', '* Exterior Siding', '* Window Pane',
       '* Deck/Porch On Grade', '* Deck/Porch Elevated',
       '* Patio Cover/Carport Attached to Structure',
       'Distance - Propane Tank to Structure',
       'Distance - Residence to Utility/Misc Structure &gt; 120 SQFT', 
        'Year Built (parcel)', 'Latitude', 'Longitude', 'x', 'y']

#grab individual parts from the json data
features = [input_data[identifier] for identifier in list_yay]

#convert incoming json to
df = pd.DataFrame([input_data])

#apply same one-hot encoding (same columns, same order)
with open("columns_used_in_training.json") as f:
    columns = json.load(f)

df_encoded = pd.get_dummies(df).reindex(columns=columns, fill_value=0)

#predict
prediction = classifier.predict(df_encoded)
print(prediction)