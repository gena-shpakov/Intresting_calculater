from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/latest-version')
def latest_version():
    # Тут ти вказуєш актуальні дані про версію
    data = {
        "version": "1.0.1",
        "changelog": "- Виправлено баги\n- Додано нові функції",
        "download_url": "https://example.com/downloads/your_program_1.0.1.exe"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
