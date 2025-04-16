import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from utils.email_connector import EmailConnector
from utils.email_parser import EmailParser
from controllers.email_controller import EmailController

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    email_connector = EmailConnector(
        server=data.get('server') or os.getenv('EMAIL_SERVER'),
        port=data.get('port') or os.getenv('EMAIL_PORT'),
        email=data.get('email') or os.getenv('EMAIL_USER'),
        password=data.get('password') or os.getenv('EMAIL_PASSWORD')
    )
    
    try:
        connection_status = email_connector.connect()
        return jsonify({'status': 'success', 'message': connection_status})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/fetch-emails', methods=['POST'])
def fetch_emails():
    data = request.json
    controller = EmailController()
    
    try:
        emails = controller.fetch_emails(
            folder=data.get('folder', 'INBOX'),
            limit=data.get('limit', 10),
            criteria=data.get('criteria', 'ALL')
        )
        return jsonify({'status': 'success', 'emails': emails})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/parse-email', methods=['POST'])
def parse_email():
    data = request.json
    email_content = data.get('email_content', '')
    
    try:
        parser = EmailParser()
        parsed_data = parser.parse(email_content)
        return jsonify({'status': 'success', 'parsed_data': parsed_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/export', methods=['POST'])
def export_data():
    data = request.json
    format_type = data.get('format', 'csv')
    parsed_data = data.get('parsed_data', [])
    
    controller = EmailController()
    
    try:
        export_result = controller.export_data(parsed_data, format_type)
        return jsonify({'status': 'success', 'export_path': export_result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 