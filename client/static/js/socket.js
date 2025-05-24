const socket = io(); // Kết nối WebSocket đến server mặc định

// Khi kết nối thành công
socket.on('connect', () => {
    console.log('Connected, joining room...');
    const clientId = 'receiver1'; // Thay clientId thực tế
    socket.emit('join', { client_id: clientId });
});

// Nhận file được gửi
socket.on('receive_encrypted_file', (data) => {
    console.log('Received encrypted file:', data);
    // Xử lý giải mã, xác thực ở bước tiếp theo
});

// Gửi file (sender)
function sendEncryptedFile(toClientId, fileDataBase64, signatureBase64, filename) {
    socket.emit('send_encrypted_file', {
        to_client_id: toClientId,
        file_data: fileDataBase64,
        signature: signatureBase64,
        filename: filename
    });
}

// Gửi sự kiện join room
function joinRoom(clientId) {
    socket.emit('join', { client_id: clientId });
    console.log(`Joined room: ${clientId}`);
}

// Lắng nghe sự kiện nhận file
function onReceiveEncryptedFile(callback) {
    socket.on('receive_encrypted_file', callback);
}

// Gửi file mã hóa + chữ ký
function sendEncryptedFile(data) {
    socket.emit('send_encrypted_file', data);
}
