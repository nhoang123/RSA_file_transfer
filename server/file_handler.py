import os

def save_temp_file(file_data: bytes, filename: str, temp_dir: str = '/tmp'):
    """
    Lưu file nhị phân tạm thời, trả về đường dẫn file lưu.
    """
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)
    return file_path

def delete_file(filepath: str):
    """
    Xóa file nếu tồn tại
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"[ERROR] Xóa file lỗi: {e}")
    return False
