class ClientKey:
    def __init__(self, client_id: str, public_key_path: str):
        self.client_id = client_id
        self.public_key_path = public_key_path

# Giả sử dùng dict để quản lý nhanh trong bộ nhớ (nên dùng DB khi mở rộng)
client_keys = {}

def add_or_update_client_key(client_id: str, public_key_path: str):
    client_keys[client_id] = ClientKey(client_id, public_key_path)

def get_client_public_key_path(client_id: str):
    client = client_keys.get(client_id)
    if client:
        return client.public_key_path
    return None
