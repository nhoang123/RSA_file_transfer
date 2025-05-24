// main.js

// --- SENDER ---

// Hiển thị nội dung file khi chọn
document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('fileContent').value = e.target.result;
    };
    reader.readAsText(file);
});

// Nút gửi
document.getElementById('sendBtn').addEventListener('click', async () => {
    const content = document.getElementById('fileContent').value;
    const privateKeyPEM = document.getElementById('privateKeyInput').value;
    const receiverId = document.getElementById('receiverId').value.trim();

    if (!content || !privateKeyPEM || !receiverId) {
        alert('Vui lòng nhập đầy đủ nội dung file, khóa private và ID người nhận!');
        return;
    }

    try {
        // 1. Ký nội dung
        const signatureHex = signData(privateKeyPEM, content);

        // 2. Lấy public key người nhận (demo lấy từ server hoặc input tạm)
        // TODO: Thực tế cần gọi API lấy public key receiver
        const receiverPublicKeyPEM = await fetchPublicKey(receiverId);

        // 3. Mã hóa nội dung
        const encryptedB64 = encryptWithPublicKey(receiverPublicKeyPEM, content);

        // 4. Gửi qua WebSocket
        sendEncryptedFile({
            to_client_id: receiverId,
            file_data: encryptedB64,
            signature: signatureHex,
            filename: 'file.txt'
        });

        document.getElementById('statusMessage').innerText = "Đã gửi file thành công!";

    } catch (error) {
        alert('Lỗi trong quá trình xử lý: ' + error.message);
    }
});

// Hàm demo lấy public key (thay bằng API thực tế)
async function fetchPublicKey(clientId) {
    // Giả sử API: /get_public_key?client_id=xxx trả về PEM
    const resp = await fetch(`/get_public_key?client_id=${clientId}`);
    if (!resp.ok) throw new Error('Không lấy được public key người nhận');
    const data = await resp.json();
    return data.public_key_pem;
}

// --- RECEIVER ---

document.getElementById('joinRoomBtn').addEventListener('click', () => {
    const clientId = document.getElementById('clientIdInput').value.trim();
    if (!clientId) {
        alert('Nhập ID của bạn để kết nối');
        return;
    }
    joinRoom(clientId);
    document.getElementById('fileSection').style.display = 'block';
    document.getElementById('statusMessage').innerText = 'Đã kết nối với server.';
});

// Khi nhận file mã hóa
onReceiveEncryptedFile(async (data) => {
    const { file_data, signature, filename } = data;

    const privateKeyPEM = prompt('Nhập khóa private của bạn để giải mã:');
    if (!privateKeyPEM) {
        alert('Cần khóa private để giải mã file!');
        return;
    }

    try {
        // Giải mã nội dung
        const decrypted = decryptWithPrivateKey(privateKeyPEM, file_data);

        // Lấy public key người gửi (giả sử có sẵn hoặc API)
        const senderPublicKeyPEM = await fetchPublicKey(data.from_client_id || 'sender'); // sửa theo thực tế

        // Xác thực chữ ký
        const verified = verifySignature(senderPublicKeyPEM, decrypted, signature);

        // Hiển thị
        document.getElementById('receivedFileContent').value = decrypted;

        document.getElementById('signatureStatus').innerText = verified
            ? 'Chữ ký hợp lệ ✅'
            : 'Chữ ký không hợp lệ hoặc file bị thay đổi ❌';

        // Hiển thị trạng thái cảnh báo nếu cần

    } catch (e) {
        alert('Lỗi khi giải mã hoặc xác thực chữ ký: ' + e.message);
    }
});

// Nút tải file xuống
document.getElementById('downloadBtn').addEventListener('click', () => {
    const content = document.getElementById('receivedFileContent').value;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'downloaded_file.txt';
    a.click();

    URL.revokeObjectURL(url);
});
