from Crypto.PublicKey import RSA
import os

KEY_DIR = os.path.join(os.path.dirname(__file__), 'keys')

def generate_rsa_keypair(key_size=2048):
    """
    Tạo cặp khóa RSA (private + public)
    """
    key = RSA.generate(key_size)
    return key

def save_key_to_file(key, filepath):
    """
    Lưu private hoặc public key ra file PEM
    """
    with open(filepath, 'wb') as f:
        f.write(key.export_key('PEM'))

def load_key_from_file(filepath):
    """
    Đọc private hoặc public key từ file PEM
    """
    with open(filepath, 'rb') as f:
        key_data = f.read()
    key = RSA.import_key(key_data)
    return key

def get_public_key_pem(key):
    """
    Lấy public key dạng PEM từ private key hoặc public key object
    """
    if key.has_private():
        public_key = key.publickey()
    else:
        public_key = key
    return public_key.export_key('PEM')

def save_public_key_pem(pem_bytes, filepath):
    with open(filepath, 'wb') as f:
        f.write(pem_bytes)

def ensure_key_dir():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

# Hàm tiện ích tạo và lưu khóa mặc định cho server (chạy 1 lần)
def generate_and_save_server_keys():
    ensure_key_dir()
    priv_key_path = os.path.join(KEY_DIR, 'server_private.pem')
    pub_key_path = os.path.join(KEY_DIR, 'server_public.pem')

    if not os.path.exists(priv_key_path) or not os.path.exists(pub_key_path):
        key = generate_rsa_keypair()
        save_key_to_file(key, priv_key_path)
        pub_pem = get_public_key_pem(key)
        save_public_key_pem(pub_pem, pub_key_path)
        print(f"[INFO] Server RSA keypair generated and saved in {KEY_DIR}")
    else:
        print("[INFO] Server RSA keypair already exists.")

if __name__ == "__main__":
    generate_and_save_server_keys()
