import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve, confusion_matrix, accuracy_score, f1_score, precision_score, \
    roc_curve, roc_auc_score
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
import joblib
import os


# print(sklearn.__version__)
# Usage:
# data_path = '/content/train.csv'
# train=Train('/content/train.csv', result_dir)

class Train:
    def __init__(self, data_path, result_dir):
        self.data_path = data_path
        self.result_dir = result_dir
        self.model_subfolder = os.path.join(self.result_dir, "pkl")
        self.df = pd.read_csv(self.data_path)
        self.feature_cols = [
            'PageVisit_errorCount',
            'PageVisit_isBlank',
            'pageActiveDuration',
            'pageDuration',
            'PageVisit_timeSinceSessionStart',
            'LCP',
            'pageLoad',
            'FirstInteration_timeSinceSessionStart',
            'FID',
            'TextInput_timeSinceSessionStart',
            'TextInputTime',
            'ElementClick_errorCount',
            'ElementClick_repeatClick',
            'ElementClick_timeSinceSessionStart',
            'feedbackInterval',
            'slowNeChinaork',
            'WindowResizing_timeSinceSessionStart',
            'WindowResizing_viewportHeightChangeRate',
            'WindowResizing_viewporChinaidthChangeRate',
            'ViewportStay_timeSinceSessionStart']
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

    def train(self):
        data_path = self.data_path

        df = pd.read_csv(data_path)

        # Choose cols as features
        features = df[self.feature_cols]

        # Choose cols as targets
        targets = df[self.target_cols]

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.3, random_state=42)
        classifiers = {}
        for col in self.target_cols:
            clf = RandomForestClassifier(n_estimators=300, criterion="gini", random_state=42)
            clf.fit(X_train, y_train[col])
            classifiers[col] = clf
            # Save the trained model
            model_save_path = os.path.join(self.model_subfolder, f"{col}_model.pkl")
            joblib.dump(clf, model_save_path)

        # Predict on test set for each target column
        y_preds = {}
        y_preds_proba = {}
        for col, clf in classifiers.items():
            y_pred = clf.predict(X_test)
            y_preds[col] = y_pred
            if len(clf.classes_) == 2:  # Check if there are two classes
                y_pred_proba = clf.predict_proba(X_test)[:, 1]
            else:  # If only one class, use the probability of that class
                y_pred_proba = clf.predict_proba(X_test)[:, 0]
            y_preds_proba[col] = y_pred_proba

        # Calculate accuracy for each target column
        accuracies = {}
        for col in self.target_cols:
            accuracies[col] = accuracy_score(y_test[col], y_preds[col])
            print(f"Accuracy for {col}: {accuracies[col]}")

        # Calculate overall accuracy (average accuracy across all target columns)
        overall_accuracy = np.mean(list(accuracies.values()))

        print("Overall Accuracy:", overall_accuracy)

        plt.figure(figsize=(15, 10))
        colors = sns.color_palette("husl", len(self.target_cols))

        # Combined Precision-Recall Curve
        for i, col in enumerate(self.target_cols):
            if len(np.unique(y_test[col])) == 2:
                precision, recall, _ = precision_recall_curve(y_test[col], y_preds_proba[col])
                plt.plot(recall, precision, label=f'{col}', color=colors[i])

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Combined Precision-Recall Curve')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.result_dir, "combined_precision_recall_curve.png"))
        plt.show()

        # Combined F1 Score Curve
        plt.figure(figsize=(15, 10))
        for i, col in enumerate(self.target_cols):
            if len(np.unique(y_test[col])) == 2:
                precision, recall, thresholds = precision_recall_curve(y_test[col], y_preds_proba[col])
                f1_scores = 2 * (precision * recall) / (precision + recall + 1e-6)  # Avoid division by zero
                plt.plot(thresholds, f1_scores[:-1], label=f'{col}', color=colors[i])

        plt.xlabel('Threshold')
        plt.ylabel('F1 Score')
        plt.title('Combined F1 Score Curve')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.result_dir, "combined_f1_score_curve.png"))
        plt.show()

        # Combined ROC Curve
        plt.figure(figsize=(15, 10))
        for i, col in enumerate(self.target_cols):
            fpr, tpr, _ = roc_curve(y_test[col], y_preds_proba[col])
            roc_auc = roc_auc_score(y_test[col], y_preds_proba[col])
            plt.plot(fpr, tpr, label=f'{col} (AUC={roc_auc:.2f})', color=colors[i])

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Combined ROC Curves')
        plt.legend()
        plt.savefig(os.path.join(self.result_dir, "combined_roc_curves.png"))
        plt.show()

        # Combined Calibration Curve
        plt.figure(figsize=(15, 10))
        for i, col in enumerate(self.target_cols):
            prob_true, prob_pred = calibration_curve(y_test[col], y_preds_proba[col], n_bins=10)
            plt.plot(prob_pred, prob_true, label=f'{col}', color=colors[i])

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('Predicted Probability')
        plt.ylabel('Fraction of Positives')
        plt.title('Combined Calibration Curves')
        plt.legend()
        plt.savefig(os.path.join(self.result_dir, "combined_calibration_curves.png"))
        plt.show()

        # Plot combined confusion matrix (This could be very large with 9 targets)
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))  # Adjust subplot grid as needed
        axes = axes.flatten()
        for i, col in enumerate(self.target_cols):
            cm = confusion_matrix(y_test[col], y_preds[col])
            sns.heatmap(cm, annot=True, fmt='d', ax=axes[i], cmap='Blues')
            axes[i].set_title(col)
            axes[i].set_xlabel('Predicted')
            axes[i].set_ylabel('Actual')
        plt.tight_layout()
        plt.savefig(os.path.join(self.result_dir, "combined_confusion_matrix.png"))
        plt.show()
