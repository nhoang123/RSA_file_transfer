# Secure File Transfer - Hệ Thống Truyền File Bảo Mật với RSA và Chữ Ký Số

## Mô tả dự án

Ứng dụng web truyền file bảo mật giữa client và server sử dụng:

- **Mã hóa RSA** để đảm bảo chỉ người nhận mới đọc được file  
- **Chữ ký số (Digital Signature)** để xác thực người gửi và kiểm tra tính toàn vẹn file  
- **Giao tiếp WebSocket realtime** giữa client và server  
- Giao diện thân thiện cho người gửi và người nhận

---

## Cấu trúc thư mục

secure-file-transfer/
├── server/
│ ├── app.py # Flask server chính, chạy WebSocket
│ ├── crypto_utils.py # Hàm mã hóa, giải mã, ký số
│ ├── key_manager.py # Quản lý khóa RSA (tạo, lưu, load)
│ ├── file_handler.py # Xử lý file (nếu có)
│ ├── socket_events.py # Sự kiện WebSocket (nếu tách riêng)
│ ├── models.py # Mô hình dữ liệu (nếu dùng)
│ ├── constants.py # Hằng số chung
│ ├── keys/ # Thư mục chứa khóa private/public server và client
│ └── tests/ # Thư mục chứa các file test
├── client/
│ ├── static/
│ │ ├── css/
│ │ │ └── style.css # Style cho giao diện
│ │ ├── js/
│ │ │ ├── crypto.js # Mã hóa, ký số phía client
│ │ │ ├── socket.js # Quản lý WebSocket client
│ │ │ └── main.js # Logic chính giao diện client
│ └── templates/
│ ├── index.html # Trang chính
│ ├── sender.html # Giao diện người gửi
│ └── receiver.html # Giao diện người nhận
├── requirements.txt # Danh sách thư viện Python cần cài
└── README.md # File hướng dẫn này

yaml
Copy

---

## Yêu cầu

- Python 3.7 trở lên  
- Thư viện Python: Flask, Flask-SocketIO, pycryptodome, eventlet  
- Trình duyệt hiện đại hỗ trợ WebSocket và JavaScript

---

## Hướng dẫn cài đặt và chạy

### 1. Tạo môi trường ảo và cài dependencies

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows CMD

pip install -r requirements.txt
2. Tạo khóa RSA cho server (chạy 1 lần)
bash
Copy
python server/key_manager.py
3. Tạo khóa client
Chạy script tương tự key_manager.py trên client hoặc tạo khóa thủ công

Đảm bảo client giữ private key an toàn và upload public key lên server qua API

4. Chạy server Flask
bash
Copy
python server/app.py
Server chạy tại địa chỉ: http://localhost:5000

Cách sử dụng giao diện
Trang chính
Truy cập http://localhost:5000/ để vào trang chính

Chọn vào “Giao diện Người gửi” hoặc “Giao diện Người nhận”

Giao diện Người gửi
Chọn file cần gửi

Nội dung file sẽ hiển thị trong ô có thể chỉnh sửa

Nhập ID người nhận (client_id)

Dán khóa private PEM của bạn để ký file

Nhấn nút Ký, Mã hóa và Gửi

File được mã hóa bằng khóa public người nhận, ký bằng private key bạn nhập và gửi qua WebSocket đến server

Giao diện Người nhận
Nhập ID của bạn (client_id)

Nhấn nút Kết nối để tham gia phòng nhận file

Khi có file gửi đến, bạn sẽ được hỏi dán khóa private PEM để giải mã file

Nội dung file sau giải mã hiển thị trên giao diện

Trạng thái chữ ký số được hiển thị (hợp lệ hoặc không hợp lệ)

Bạn có thể tải file đã giải mã về máy

Kiến trúc kỹ thuật
Mã hóa RSA: File được mã hóa bằng public key người nhận.

Chữ ký số: Hash file (SHA-256) được ký bằng private key người gửi.

WebSocket: Dùng Flask-SocketIO để kết nối realtime giữa client và server.

Quản lý khóa: Khóa RSA được lưu trữ an toàn trên server và client.

Client: Xử lý mã hóa, ký, giải mã, xác thực bằng thư viện JS (ví dụ jsrsasign).

Server: Chuyển tiếp dữ liệu giữa các client thông qua WebSocket.

API chính
POST /upload_client_public_key : Upload public key client lên server

GET /get_public_key?client_id=xxx : Lấy public key client theo id (dùng khi mã hóa hoặc xác thực)

WebSocket event:

'join': client gửi để tham gia phòng

'send_encrypted_file': gửi file mã hóa + chữ ký

'receive_encrypted_file': server phát lại file cho client nhận

Ghi chú quan trọng
Bảo mật khóa private: Tuyệt đối không gửi hoặc lưu khóa private lên server

Xác thực client: Cần bổ sung xác thực (token, login) để tránh giả mạo client_id

Kích thước file: RSA chỉ mã hóa file nhỏ, với file lớn cần hybrid encryption (AES + RSA)

CORS: Trong phát triển cho phép cors_allowed_origins="*", khi deploy cần cấu hình lại

Phần mở rộng
Mã hóa file lớn với hybrid AES + RSA

Giao diện nâng cao, upload file nhiều định dạng, đa phần chunk file lớn

Lưu lịch sử truyền file trên server hoặc database

Hệ thống xác thực, phân quyền người dùng