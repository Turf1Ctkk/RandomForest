from FeatureExtractor import FeatureExtractor
from train import Train
from Inference import Inference

# To test the code

# Folder/file format
# root
#   Inference
#       json
#           log1.json
#       pkl
#           file.pkl
#       result.csv
#   Train
#       train.csv
#       run
#           pkl

json_folder = "E:\\HDU\\OutSource\\Inference\\json"
csv_file_path = "E:\\HDU\\OutSource\\Inference\\result.csv"
data_path = "E:\\HDU\\OutSource\\Train\\train.csv"
model_dir = "E:\\HDU\\OutSource\\Inference\\pkl"
result_dir = "E:\\HDU\\OutSource\\Train\\run"

# Feature Extract
extractor = FeatureExtractor(json_folder, csv_file_path)
extractor.extract_features()

# Train
trainer = Train(data_path, result_dir)
trainer.train()

# Inference
result = Inference(model_dir, csv_file_path)
all_predictions, all_probability_percentages = result.predict()
for i in range(len(all_predictions)):
        print(f'Row {i + 1} Predictions:')
        print(all_predictions[i])
        print(f'Row {i + 1} Probability Percentages:')
        for target_name, percentage in all_probability_percentages[i].items():
            print(f'{target_name}: {percentage:.2f}%')