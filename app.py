from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Device Status Storage
status = {
    "light1": "OFF",
    "light2": "OFF",
    "light3": "OFF",
    "light4": "OFF",
    "fanSpeed": 0
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "ESP32 REST API Running"})


# MAIN CONTROL ENDPOINT
@app.route("/set", methods=["POST"])
def set_device():
    data = request.get_json()

    # SAFETY CHECK
    if data is None:
        return jsonify({"error": "No JSON received"}), 400

    # --------------------------
    # FAN SPEED HANDLING
    # --------------------------
    if data.get("cmd") == "FAN":
        speed = int(data.get("speed", 0))

        if speed < 0 or speed > 5:
            return jsonify({"error": "Invalid speed (0–5 only)"}), 400

        status["fanSpeed"] = speed

        print(f"Fan Speed Updated → {speed}")

        return jsonify({
            "status": "OK",
            "device": "fan",
            "fanSpeed": speed
        })

    # --------------------------
    # LIGHT HANDLING
    # --------------------------
    device = data.get("device")
    state = data.get("state")

    if device in ["light1", "light2", "light3", "light4"]:
        if state not in ["ON", "OFF"]:
            return jsonify({"error": "State must be ON or OFF"}), 400

        status[device] = state

        print(f"{device} → {state}")

        return jsonify({
            "status": "OK",
            "device": device,
            "state": state
        })

    return jsonify({"error": "Invalid command"}), 400


# STATUS PAGE (OPTIONAL)
@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(status)


# RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
