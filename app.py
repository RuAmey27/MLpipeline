from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load latest model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Serves the HTML template

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return jsonify({"prediction": prediction})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    df = pd.DataFrame([data])
    df.to_csv("data/feedback_data.csv", mode="a", header=False, index=False)
    return jsonify({"message": "Feedback received"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
