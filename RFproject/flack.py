from flask import Flask, request, jsonify
import pandas as pd
import joblib
from FeatureExtractor import FeatureExtractor
from Inference import Inference
from train import Train
import os

app = Flask(__name__)

@app.route('/train', methods=['POST'])
def train():
    data_path = request.form.get('data_path')
    result_dir = request.form.get('result_dir')
    model_dir = os.path.join(result_dir, 'models')

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    trainer = Train(data_path, model_dir, result_dir)
    trainer.train()

    return jsonify({'message': 'Training completed successfully'})

@app.route('/predict', methods=['POST'])
def predict():
    json_folder = request.form.get('json_folder')
    csv_file_path = request.form.get('csv_file_path')
    model_dir = request.form.get('model_dir')

    extractor = FeatureExtractor(json_folder, csv_file_path)
    extractor.extract_features()

    new_data = pd.read_csv(csv_file_path)
    inference = Inference(model_dir)
    predictions = inference.predict(new_data)

    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)