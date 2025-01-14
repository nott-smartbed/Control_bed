from machine import Pin, UART
import uasyncio as asyncio
from utime import sleep

# Cấu hình cổng UART
UART_ID = 1
BAUD_RATE = 9600
TX_PIN = 17
RX_PIN = 18

# Khởi tạo UART
uart = UART(UART_ID, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, bits=8, parity=None, stop=1)

# Bộ đệm để lưu dữ liệu chưa hoàn chỉnh
buffer = ""

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


async def receive_data():
    """
    Nhận dữ liệu qua UART và chỉ in khi dữ liệu đầy đủ (chứa dấu [ và ]).
    """
    global buffer
    while True:
        if uart.any():  # Kiểm tra nếu có dữ liệu
            try:
                raw_data = uart.read().decode('utf-8')  # Đọc và giải mã dữ liệu
                buffer += raw_data  # Thêm dữ liệu mới vào bộ đệm

                # Kiểm tra nếu dữ liệu đủ dấu [ và ]
                if "[" in buffer and "]" in buffer:
                    start = buffer.find("[")
                    end = buffer.find("]") + 1
                    full_data = buffer[start:end]  # Lấy dữ liệu đầy đủ
                    complete_data = process_input(full_data)
                    print(f"Received: {complete_data}")  # In ra dữ liệu đầy đủ
                    buffer = buffer[end:]  # Loại bỏ dữ liệu đã xử lý khỏi bộ đệm
            except UnicodeError:
                print("Received invalid data (non-UTF-8).")
        await asyncio.sleep(0.1)  # Chờ trước khi kiểm tra tiếp

async def send_data(data):
    """
    Gửi dữ liệu qua UART.
    """
    uart.write(data + "\n")  # Thêm ký tự xuống dòng để phân tách dữ liệu
    print(f"Sent: {data}")
    await asyncio.sleep(0)  # Chờ cho phép xử lý các tác vụ khác

async def main():
    """
    Chương trình chính để gửi và nhận dữ liệu.
    """
    # Gửi dữ liệu ví dụ (có thể thay đổi nội dung)
    await send_data("Hello ESP!")
    
    # Nhận dữ liệu qua UART
    await receive_data()

# Chạy chương trình chính
asyncio.run(main())

