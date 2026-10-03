from flask import Flask, request, jsonify
import joblib
import os
from twilio.rest import Client

app = Flask(__name__)

# ML Model
model = joblib.load("model.pkl")

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
FARMER_WHATSAPP_TO = os.getenv("FARMER_WHATSAPP_TO")


def send_whatsapp(message):

    client = Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN
    )

    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=FARMER_WHATSAPP_TO,
        body=message
    )


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

    # WhatsApp only for risk cases
    if prediction in ["SUSPECTED", "HIGH RISK"]:

        message = f"""🚨 SMART MILK ANALYZER ALERT

Milk Sample Risk: {prediction}

pH: {ph}
Temperature: {temperature} °C
TDS: {tds}

Please check the animal and take appropriate veterinary action."""

        try:
            send_whatsapp(message)
            whatsapp_status = "Message sent"
        except Exception as e:
            whatsapp_status = "Message failed"
            print("WhatsApp Error:", e)

    else:
        whatsapp_status = "No alert required"


    return jsonify({
        "pH": ph,
        "Temperature": temperature,
        "TDS": tds,
        "Risk": prediction,
        "WhatsApp": whatsapp_status
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )