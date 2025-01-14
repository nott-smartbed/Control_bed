import requests
import logging
import time

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thay đổi URL và token của bạn
HA_URL = "http://192.168.100.42:8123/api/states"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjZGE0OTdhN2QyNWM0NjYxOTgzMmJhNGJhOGNlYmE2NiIsImlhdCI6MTczNjc0ODQzMywiZXhwIjoyMDUyMTA4NDMzfQ.MF7qOcUrcbvrLELABfxlLqXLDDjjSGER57TbKUA6E7U"

# Khởi tạo từ điển để lưu trữ giá trị trước đó
previous_states = {}

def fetch_states():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(HA_URL, headers=headers)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        states = response.json()
        valid_entity_ids = [
            'input_number.head',
            'input_number.lean',
            'input_number.foot',
            'input_boolean.mode_1',
            'input_boolean.mode_2',
            'input_boolean.mode_3',
            'input_boolean.mode_4',
            'input_boolean.mode_5',
            'input_boolean.custom',
            'input_boolean.pause_continue',
            'input_boolean.start_stop'
        ]
        # In ra giá trị của các thực thể cụ thể
        for state in states:
            if state['entity_id'] in valid_entity_ids:
                current_value = state['state']
                entity_id = state['entity_id']
                
                # So sánh với giá trị trước đó
                if entity_id not in previous_states or previous_states[entity_id] != current_value:
                    logging.info(f"{entity_id}: {current_value}")
                    previous_states[entity_id] = current_value  # Cập nhật giá trị trước đó
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")

def set_values():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    entities = ['input_number.head_current', 'input_number.lean_current', 'input_number.foot_current']
    value = 60

    for entity_id in entities:
        url = f"{HA_URL}/{entity_id}"
        payload = {"state": value}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"Set {entity_id} to {value}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error setting value for {entity_id}: {e}")

if __name__ == '__main__':
    while True:
        fetch_states()
        set_values()  # Gọi hàm để đặt giá trị
        time.sleep(5)  # Lặp lại mỗi 60 giây
