from Crypto.PublicKey import RSA
from crypto_utils import encrypt_rsa, decrypt_rsa, sign_data, verify_signature

def test_rsa_crypto_and_signature():
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()

    message = b"Hello RSA encryption and signing!"

    # Mã hóa
    encrypted = encrypt_rsa(public_key, message)
    # Giải mã
    decrypted = decrypt_rsa(private_key, encrypted)
    assert decrypted == message
    print("Encrypt/Decrypt OK")

    # Ký
    signature = sign_data(private_key, message)
    # Xác thực đúng
    assert verify_signature(public_key, message, signature) is True
    print("Signature verify OK")

    # Xác thực sai (thay đổi message)
    assert verify_signature(public_key, b"Fake message", signature) is False
    print("Signature detect tamper OK")

if __name__ == "__main__":
    test_rsa_crypto_and_signature()
