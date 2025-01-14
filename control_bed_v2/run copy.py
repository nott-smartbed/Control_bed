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
        
        # In ra giá trị của các thực thể cụ thể
        for state in states:
            if state['entity_id'] in ['input_number.head', 'input_number.lean', 'input_number.foot']:
                current_value = state['state']
                entity_id = state['entity_id']
                
                # So sánh với giá trị trước đó
                if entity_id not in previous_states or previous_states[entity_id] != current_value:
                    logging.info(f"{entity_id}: {current_value}")
                    previous_states[entity_id] = current_value  # Cập nhật giá trị trước đó
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")

if __name__ == '__main__':
    while True:
        fetch_states()
        # time.sleep(60)  # Lặp lại mỗi 60 giây