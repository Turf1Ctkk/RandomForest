import pandas as pd
import joblib
import os


# model_dir='/content/run2/pkl/'
# Usage:
# result = Inference(model_dir,csv_file_path)
# all_predictions, all_probability_percentages = result.predict()
class Inference:
    def __init__(self, model_dir, csv_file_path):
        self.model_dir = model_dir
        self.csv_file_path = csv_file_path
        self.target_cols = [
            'NoResponseWhenCicking',
            'HighBounceRate',
            'RepeatClick',
            'SlowPageOpening',
            'SlowWebFeedbackAfterClicking',
            'ClickError',
            'PageLoadError',
            'PageLoadBlank',
            'MultipleSimultaneousOccurrences'
        ]

    def predict(self):
        model_filenames = [
            os.path.join(self.model_dir, f'{col}_model.pkl') for col in self.target_cols
        ]
        models = {name: joblib.load(os.path.join(self.model_dir, filename)) for name, filename in
                  zip(self.target_cols, model_filenames)}

        new_data = pd.read_csv(self.csv_file_path)

        all_predictions = []
        all_probability_percentages = []

        for index, row in new_data.iterrows():
            row_data = row.to_frame().transpose()
            predictions = {}
            probability_percentages = {}

            for target_name, model in models.items():
                predictions[target_name] = model.predict(row_data)[0]
                prediction_proba = model.predict_proba(row_data)[:, 1] * 100
                probability_percentages[target_name] = prediction_proba[0]

            all_predictions.append(predictions)
            all_probability_percentages.append(probability_percentages)

        return all_predictions, all_probability_percentages