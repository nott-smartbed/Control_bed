import json
import os

# Tệp dữ liệu lưu giá trị
DATA_FILE = "/data/data.json"

# Hàm để đảm bảo tệp tồn tại
def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"lean": 0, "head": 0, "foot": 0}, f)

# Hàm lưu giá trị vào tệp
def save_values(lean, head, foot):
    ensure_data_file()
    data = {
        "lean": lean,
        "head": head,
        "foot": foot
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)
    print(f"Lưu thành công: {data}")

# Hàm tải giá trị từ tệp
def load_values():
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    print(f"Giá trị đã tải: {data}")
    return data

# Chạy thử
if __name__ == "__main__":
    # Lưu giá trị ví dụ
    save_values(lean=15, head=30, foot=10)

    # Tải giá trị
    values = load_values()
    print(f"Lean: {values['lean']}, Head: {values['head']}, Foot: {values['foot']}")
