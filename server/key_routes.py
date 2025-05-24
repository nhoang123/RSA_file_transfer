from flask import Flask, request, jsonify
import os

app = Flask(__name__)

KEYS_FOLDER = os.path.join(os.path.dirname(__file__), 'keys')
CLIENT_KEYS_FOLDER = os.path.join(KEYS_FOLDER, 'clients')

if not os.path.exists(CLIENT_KEYS_FOLDER):
    os.makedirs(CLIENT_KEYS_FOLDER)

@app.route('/upload_client_public_key', methods=['POST'])
def upload_client_public_key():
    data = request.json
    client_id = data.get('client_id')
    public_key_pem = data.get('public_key_pem')

    if not client_id or not public_key_pem:
        return jsonify({'error': 'client_id and public_key_pem are required'}), 400

    # Lưu public key client
    client_key_path = os.path.join(CLIENT_KEYS_FOLDER, f"{client_id}_public.pem")
    try:
        with open(client_key_path, 'wb') as f:
            f.write(public_key_pem.encode())
        return jsonify({'message': f'Public key for client {client_id} saved successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
