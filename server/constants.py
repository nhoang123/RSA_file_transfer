import os

# Đường dẫn thư mục chứa khóa
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, 'keys')
CLIENT_KEYS_DIR = os.path.join(KEYS_DIR, 'clients')

# Các tên file khóa mặc định server
SERVER_PRIVATE_KEY_FILE = os.path.join(KEYS_DIR, 'server_private.pem')
SERVER_PUBLIC_KEY_FILE = os.path.join(KEYS_DIR, 'server_public.pem')

# Các hằng số khác
RSA_KEY_SIZE = 2048

# Giới hạn kích thước file upload (byte) — ví dụ 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024

# Các chuỗi sự kiện WebSocket
EVENT_JOIN = 'join'
EVENT_SEND_ENCRYPTED_FILE = 'send_encrypted_file'
EVENT_RECEIVE_ENCRYPTED_FILE = 'receive_encrypted_file'
