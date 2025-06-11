from flask import Flask, request, jsonify
import base64
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = "asiunk7/pdf-watermark-server"  # ganti sesuai repo lo
GITHUB_FOLDER = "pdfs"

@app.route('/upload', methods=['POST'])
def upload_to_github():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = file.filename
    content = base64.b64encode(file.read()).decode('utf-8')

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FOLDER}/{filename}"

    payload = {
        "message": f"Upload {filename} via Adalo",
        "content": content
    }

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    res = requests.put(url, json=payload, headers=headers)

    if res.status_code in [200, 201]:
        return jsonify({"status": "uploaded", "filename": filename}), 200
    else:
        return jsonify({"error": res.json()}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
