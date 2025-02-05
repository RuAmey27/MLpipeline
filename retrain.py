import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
import os
import filecmp
import datetime

# Check if dataset has changed
if not os.path.exists("data/dataset_old.csv") or not filecmp.cmp("data/dataset.csv", "data/dataset_old.csv", shallow=False):
    print("Dataset changed. Retraining model...")
    df_main = pd.read_csv("data/dataset.csv")
    df_feedback = pd.read_csv("data/feedback_data.csv")
    df_combined = pd.concat([df_main, df_feedback], ignore_index=True)

    X = df_combined[["YearsExperience"]]
    y = df_combined["Salary"]
    model = LinearRegression()
    model.fit(X, y)

    timestamp = datetime.datetime.now().strftime("%d%m%y%H%M")
    with open(f"models/model_{timestamp}.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)

    os.replace("data/dataset.csv", "data/dataset_old.csv")
    print("Model retrained and dataset updated!")
else:
    print("No dataset changes detected. Skipping retraining.")
