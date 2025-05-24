import os
from key_manager import load_key_from_file, get_public_key_pem

KEY_DIR = os.path.join(os.path.dirname(__file__), '..', 'keys')
priv_key_path = os.path.join(KEY_DIR, 'server_private.pem')

def test_load_and_get_public():
    priv_key = load_key_from_file(priv_key_path)
    pub_pem = get_public_key_pem(priv_key)
    assert b'BEGIN PUBLIC KEY' in pub_pem
    print("Load private key and extract public key PEM: OK")

if __name__ == "__main__":
    test_load_and_get_public()
