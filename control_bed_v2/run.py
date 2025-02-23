import requests
import serial
import logging
import time


SERIAL_PORT = "/dev/ttyAMA0"
BAUDRATE = 9600
HA_URL = "http://192.168.100.42:8123/api/states"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjZGE0OTdhN2QyNWM0NjYxOTgzMmJhNGJhOGNlYmE2NiIsImlhdCI6MTczNjc0ODQzMywiZXhwIjoyMDUyMTA4NDMzfQ.MF7qOcUrcbvrLELABfxlLqXLDDjjSGER57TbKUA6E7U"

previous_states = {}

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,  # Thay đổi thành DEBUG để xem nhiều thông tin hơn
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
# Xử lý dữ liệu dùng để chuyển input dạng
def process_input(input_str):
    # Chuyển chuỗi thành list
    input_list = eval(input_str)

    output_list = []
    for item in input_list:
        if item == 'on':
            output_list.append(1)
        elif item == 'off':
            output_list.append(0)
        else:
            try:
                # Chuyển đổi các giá trị số dưới dạng chuỗi thành int (số nguyên)
                output_list.append(int(float(item)))  # Chuyển thành float trước, sau đó chuyển thành int
            except ValueError:
                # Nếu không thể chuyển đổi thành int, giữ nguyên chuỗi
                output_list.append(item)

    return output_list
def get_states():
    states_list = []
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
                states_list.append((current_value))
                # So sánh với giá trị trước đó
                if entity_id not in previous_states or previous_states[entity_id] != current_value:
                    logging.info(f"{entity_id}: {current_value}")
                    previous_states[entity_id] = current_value  # Cập nhật giá trị trước đó
                    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")

    return states_list

def set_values(value):
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    entities = ['input_number.head_current', 'input_number.lean_current', 'input_number.foot_current']

    for entity_id in entities:
        url = f"{HA_URL}/{entity_id}"
        payload = {"state": value}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"Set {entity_id} to {value}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error setting value for {entity_id}: {e}")


# while True:
#     get_states()

# Cấu hình cổng UART
SERIAL_PORT = '/dev/ttyAMA0'  # Cổng UART0 trên Orange Pi
BAUDRATE = 9600

def send_and_wait(ser, command, expected_response, timeout=0.1):
    # while True:
    # Gửi lệnh qua RS485
    ser.write(command.encode('utf-8'))
    logging.info(f"Sent: {command.strip()}")

    # Chờ phản hồi
    start_time = time.time()  # Bắt đầu tính thời gian
    while time.time() - start_time < timeout:
        if ser.in_waiting > 0:  # Nếu có dữ liệu trong buffer
            response = ser.readline().decode('utf-8').strip()
            logging.info(f"Received: {response}")
            if response == expected_response:  # Kiểm tra phản hồi đúng
                return True
    logging.warning("No valid response, resending...")  # Nếu không nhận được phản hồi đúng, gửi lại lệnh

try:
    # Mở cổng serial
    ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=0.1)
    logging.info(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")

    while True:
        logging.info(f"Gia tri: {get_states()}\n")
        send_and_wait(ser, f"{get_states()}\n", "done")

except serial.SerialException as e:
    logging.error(f"Serial error: {e}")
except KeyboardInterrupt:
    logging.info("Program interrupted by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        logging.info("Serial port closed.")