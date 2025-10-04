from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import extract_text_from_pdf, summarize_text
import os

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(file_path)

    try:
        text = extract_text_from_pdf(file_path)
        if not text.strip():
            return jsonify({"error": "PDF has no readable text"}), 400

        summary = summarize_text(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
