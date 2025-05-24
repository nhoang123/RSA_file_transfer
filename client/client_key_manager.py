from Crypto.PublicKey import RSA
import os

KEY_DIR = os.path.join(os.path.dirname(__file__), 'keys')

def generate_rsa_keypair(key_size=2048):
    key = RSA.generate(key_size)
    return key

def save_key_to_file(key, filepath):
    with open(filepath, 'wb') as f:
        f.write(key.export_key('PEM'))

def get_public_key_pem(key):
    if key.has_private():
        public_key = key.publickey()
    else:
        public_key = key
    return public_key.export_key('PEM')

def generate_and_save_client_keys():
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

    priv_key_path = os.path.join(KEY_DIR, 'client_private.pem')
    pub_key_path = os.path.join(KEY_DIR, 'client_public.pem')

    if not os.path.exists(priv_key_path) or not os.path.exists(pub_key_path):
        key = generate_rsa_keypair()
        save_key_to_file(key, priv_key_path)
        pub_pem = get_public_key_pem(key)
        save_key_to_file(key.publickey(), pub_key_path)
        print(f"[INFO] Client RSA keypair generated and saved in {KEY_DIR}")
    else:
        print("[INFO] Client RSA keypair already exists.")

if __name__ == "__main__":
    generate_and_save_client_keys()
