from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def encrypt_rsa(public_key, data_bytes):
    """
    Mã hóa data_bytes bằng public_key RSA.
    """
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(data_bytes)
    return encrypted

def decrypt_rsa(private_key, encrypted_bytes):
    """
    Giải mã encrypted_bytes bằng private_key RSA.
    """
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(encrypted_bytes)
    return decrypted

def sign_data(private_key, data_bytes):
    """
    Tạo chữ ký số trên data_bytes bằng private_key.
    """
    h = SHA256.new(data_bytes)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def verify_signature(public_key, data_bytes, signature_bytes):
    """
    Xác thực chữ ký signature_bytes của data_bytes bằng public_key.
    Trả về True nếu đúng, False nếu sai.
    """
    h = SHA256.new(data_bytes)
    try:
        pkcs1_15.new(public_key).verify(h, signature_bytes)
        return True
    except (ValueError, TypeError):
        return False
