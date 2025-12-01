from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ----- Device states -----
status = {
    "light1": "OFF",
    "light2": "OFF",
    "light3": "OFF",
    "light4": "OFF",
    "fanSpeed": 0,  # 0 to 5
    "heater": "OFF"
}

# Home endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "ESP32 REST API Running"})


# Get current status
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(status)


# Update device status
@app.route("/set", methods=["POST"])
def set_device():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # ----- Lights -----
    for i in range(1, 5):
        key = f"light{i}"
        if key in data and data[key] in ["ON", "OFF"]:
            status[key] = data[key]

    # ----- Fan -----
    if "fanSpeed" in data:
        speed = int(data["fanSpeed"])
        if speed < 0: speed = 0
        if speed > 5: speed = 5
        status["fanSpeed"] = speed

    # ----- Heater -----
    if "heater" in data and data["heater"] in ["ON", "OFF"]:
        status["heater"] = data["heater"]

    return jsonify({"status": "OK", "current": status})


if __name__ == "__main__":
    # Render automatically sets PORT via environment variable
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
