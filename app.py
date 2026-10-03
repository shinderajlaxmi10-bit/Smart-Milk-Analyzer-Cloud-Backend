from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load ML model
model = joblib.load("model.pkl")


@app.route("/")
def home():
    return "Smart Milk Analyzer ML Server is Running"


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    ph = float(data["pH"])
    temperature = float(data["Temperature"])
    tds = float(data["TDS"])

    prediction = model.predict([
        [ph, temperature, tds]
    ])[0]

    return jsonify({
        "pH": ph,
        "Temperature": temperature,
        "TDS": tds,
        "Risk": prediction
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)