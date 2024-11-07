import os

from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text
import io
from app.IA.chatIA import get_bedrock_response
from app.IA.openIA import get_chatgpt_response
from app.database.db import create_connection

from app.routes.project_routes import project_bp
from app.routes.messages_routes import msg_bp

app = Flask(__name__)
app.secret_key = os.urandom(256)

app.register_blueprint(project_bp)
app.register_blueprint(msg_bp)


@app.route('/read-pdf', methods=['POST'])
def read_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        text = extract_text(file)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    # Validación para 'file'
    if 'file' not in request.files:
        return jsonify({'error': 'File not found'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Validación para 'question'
    if 'question' not in request.form:
        return jsonify({'error': 'No question provided'})
    question = request.form['question']

    # if file:
    # Leer el contenido del archivo PDF
    #    pdf_text = extract_text(io.BytesIO(file.read()))
    #    return jsonify({'Content file': pdf_text, 'Question': question})

    if file:
        # Leer el contenido del archivo PDF
        pdf_text = extract_text(io.BytesIO(file.read()))
        finally_question = "basado en " + pdf_text + question
        bedrock_response = get_bedrock_response(finally_question)
        return jsonify({'Content file': pdf_text, 'Question': question, 'Bedrock Response': bedrock_response})


@app.route('/ask', methods=['POST'])
def ask_question():
    if 'question' not in request.form:
        return jsonify({'error': 'No question provided'})
    question = request.form['question']
    bedrock_response = get_chatgpt_response(question)
    return jsonify({'Question': question, 'IA Response': bedrock_response})


app = Flask(__name__)
