import sys
import joblib
import json

classification_model = joblib.load('models/classifymodel_2.joblib')
input_data = json.loads(sys.stdin.read())
