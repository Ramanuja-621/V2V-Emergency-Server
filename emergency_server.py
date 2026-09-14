from flask import Flask, request, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo


app = Flask(__name__)

latest_alert = {
    "vehicle_id": "NONE",
    "latitude": 0,
    "longitude": 0,
    "severity": "NONE",
    "time": "NONE"
}


@app.route("/")
def home():
    return """
    <h1>V2V Emergency Server</h1>
    <p>Server is online.</p>
    <p>Waiting for accident alerts...</p>
    <a href="/dashboard">Open Emergency Dashboard</a>
    """


@app.route("/accident", methods=["POST"])
def accident():

    global latest_alert

    data = request.get_json()

    latest_alert = {
        "vehicle_id": data.get("vehicle_id"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "severity": data.get("severity"),
        "time": datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    }

    print("\n🚨 ACCIDENT ALERT RECEIVED 🚨")
    print("Vehicle ID:", latest_alert["vehicle_id"])
    print("Latitude:", latest_alert["latitude"])
    print("Longitude:", latest_alert["longitude"])
    print("Severity:", latest_alert["severity"])

    return jsonify({
        "status": "received",
        "message": "Emergency alert received successfully"
    })


@app.route("/dashboard")
def dashboard():

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>V2V Emergency Dashboard</title>

        <meta http-equiv="refresh" content="5">

        <style>
            body {{
                font-family: Arial;
                background: #111;
                color: white;
                text-align: center;
                padding: 40px;
            }}

            .box {{
                background: #222;
                padding: 30px;
                max-width: 600px;
                margin: auto;
                border-radius: 15px;
            }}

            .danger {{
                color: red;
                font-size: 32px;
                font-weight: bold;
            }}

            .data {{
                font-size: 20px;
                margin: 15px;
            }}

            a {{
                color: #4da6ff;
            }}
        </style>
    </head>

    <body>

        <div class="box">

            <div class="danger">
                🚨 EMERGENCY DASHBOARD
            </div>

            <hr>

            <div class="data">
                Vehicle ID:
                <b>{latest_alert["vehicle_id"]}</b>
            </div>

            <div class="data">
                Severity:
                <b>{latest_alert["severity"]}</b>
            </div>

            <div class="data">
                Latitude:
                <b>{latest_alert["latitude"]}</b>
            </div>

            <div class="data">
                Longitude:
                <b>{latest_alert["longitude"]}</b>
            </div>

            <div class="data">
                Time:
                <b>{latest_alert["time"]}</b>
            </div>

        </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
