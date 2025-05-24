import os
from flask import request, jsonify
from flask_socketio import emit, join_room
from Crypto.PublicKey import RSA

from constants import CLIENT_KEYS_DIR, EVENT_JOIN, EVENT_SEND_ENCRYPTED_FILE, EVENT_RECEIVE_ENCRYPTED_FILE
from models import add_or_update_client_key

if not os.path.exists(CLIENT_KEYS_DIR):
    os.makedirs(CLIENT_KEYS_DIR)


def register_socket_events(socketio, app):
    @app.route('/upload_client_public_key', methods=['POST'])
    def upload_client_public_key():
        data = request.json
        client_id = data.get('client_id')
        public_key_pem = data.get('public_key_pem')

        if not client_id or not public_key_pem:
            return jsonify({'error': 'client_id and public_key_pem are required'}), 400

        try:
            # Kiểm tra định dạng khóa public
            RSA.import_key(public_key_pem)
        except ValueError:
            return jsonify({'error': 'Invalid public key format'}), 400

        # Lưu public key
        client_key_path = os.path.join(CLIENT_KEYS_DIR, f"{client_id}_public.pem")
        try:
            with open(client_key_path, 'wb') as f:
                f.write(public_key_pem.encode())
        except Exception as e:
            return jsonify({'error': f"Failed to save public key: {e}"}), 500

        # Cập nhật thông tin client trong bộ nhớ (hoặc DB)
        add_or_update_client_key(client_id, client_key_path)

        return jsonify({'message': f'Public key for client {client_id} saved successfully.'})

    @socketio.on(EVENT_JOIN)
    def on_join(data):
        client_id = data.get('client_id')
        if not client_id:
            emit('error', {'message': 'client_id is required to join room'})
            return
        join_room(client_id)
        emit('server_response', {'message': f'Client {client_id} joined room'})
        print(f"[SocketIO] Client {client_id} joined room")

    @socketio.on(EVENT_SEND_ENCRYPTED_FILE)
    def on_send_encrypted_file(data):
        to_client_id = data.get('to_client_id')
        if not to_client_id:
            emit('error', {'message': 'to_client_id is required'})
            return
        # Relay message to client receiving room
        socketio.emit(EVENT_RECEIVE_ENCRYPTED_FILE, data, room=to_client_id)
        print(f"[SocketIO] Relayed encrypted file to {to_client_id}")
