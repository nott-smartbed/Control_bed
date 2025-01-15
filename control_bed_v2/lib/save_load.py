import json
import logging

# Tệp JSON lưu trữ dữ liệu
FILE_PATH = "/data/data.json"

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,  # Thay đổi thành DEBUG để xem nhiều thông tin hơn
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def update_mode_values(mode, head, lean, foot):
    try:
        # Đọc dữ liệu từ tệp JSON
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)

        # Kiểm tra mode có tồn tại trong dữ liệu không
        if mode not in data:
            logging.info(f"Mode '{mode}' không tồn tại trong dữ liệu.")
            return

        # Cập nhật giá trị cho mode
        data[mode]['head'] = str(head)
        data[mode]['lean'] = str(lean)
        data[mode]['foot'] = str(foot)

        # Ghi lại dữ liệu vào tệp JSON
        with open(FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)

        logging.info(f"Cập nhật thành công cho mode '{mode}': head={head}, lean={lean}, foot={foot}")

    except FileNotFoundError:
        logging.info(f"Tệp '{FILE_PATH}' không tồn tại.")
    except json.JSONDecodeError:
        logging.info(f"Lỗi khi đọc tệp JSON '{FILE_PATH}'.")
    except Exception as e:
        logging.info(f"Lỗi không xác định: {e}")

def load_mode_values(mode):
    """
    Tải giá trị của một mode cụ thể từ file JSON.

    Args:
        mode (str): Tên của chế độ (ví dụ: "mode1", "custom1", ...)

    Returns:
        dict: Dữ liệu của mode (head, lean, foot) hoặc None nếu không tồn tại.
    """
    try:
        # Đọc dữ liệu từ tệp JSON
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)

        # Kiểm tra mode có tồn tại trong dữ liệu không
        if mode in data:
            values = data[mode]
            logging.info(f"Giá trị của mode '{mode}': head={values['head']}, lean={values['lean']}, foot={values['foot']}")
            return values
        else:
            logging.info(f"Mode '{mode}' không tồn tại trong dữ liệu.")
            return None

    except FileNotFoundError:
        logging.info(f"Tệp '{FILE_PATH}' không tồn tại.")
    except json.JSONDecodeError:
        logging.info(f"Lỗi khi đọc tệp JSON '{FILE_PATH}'.")
    except Exception as e:
        logging.info(f"Lỗi không xác định: {e}")
        return None


