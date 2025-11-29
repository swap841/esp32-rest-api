from flask import Flask, request

app = Flask(__name__)

# Store device command
device_cmd = "OFF"

@app.route("/set", methods=["POST"])
def set_cmd():
    global device_cmd
    device_cmd = request.json.get("cmd")
    return {"status": "OK", "cmd": device_cmd}

@app.route("/get", methods=["GET"])
def get_cmd():
    return {"cmd": device_cmd}

@app.route("/")
def home():
    return "ESP32 REST API Server Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
