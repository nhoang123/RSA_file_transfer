from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # thay đổi cho production
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép CORS trong dev

# Trang index demo
@app.route('/')
def index():
    return render_template('index.html')

# Các sự kiện WebSocket

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('server_response', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

# Sự kiện sender gửi file (file đã mã hóa + chữ ký)
@socketio.on('send_encrypted_file')
def handle_send_encrypted_file(data):
    """
    data dự kiến chứa:
    {
        'to_client_id': 'receiver1',
        'file_data': base64_encoded_string,
        'signature': base64_encoded_string,
        'filename': 'document.txt'
    }
    """
    to_client_id = data.get('to_client_id')
    print(f"Received encrypted file for {to_client_id}")

    # Gửi đến client nhận trong room tên to_client_id
    socketio.emit('receive_encrypted_file', data, room=to_client_id)

# Sự kiện client join room (để nhận file)
@socketio.on('join')
def handle_join(data):
    client_id = data.get('client_id')
    join_room(client_id)
    print(f"Client {client_id} joined room")
    emit('server_response', {'message': f'Joined room {client_id}'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
