from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/check_update", methods=["GET"])
def check_update():
    return jsonify({
        "latest_version": "1.0.0",
        "download_url": "https://github.com/gena-shpakov/Intresting_calculater/releases/download/v0.5.0/mysetup.exe",
        "message": "Доступна нова версія! Завантаження..."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
