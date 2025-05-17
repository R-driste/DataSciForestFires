import zipfile
import os

zip_file_path = '/Users/dristiroy/DATASCIFORESTFIRES/DataSciForestFires/archive (4).zip'
extract_to_path = '/Users/dristiroy/DATASCIFORESTFIRES/DataSciForestFires/'
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_path)
print(f"Files extracted to {extract_to_path}")
