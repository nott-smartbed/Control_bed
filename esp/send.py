import serial
import time

# Cấu hình cổng USB-RS485
SERIAL_PORT = 'COM7'  # Thay đổi thành cổng COM của bạn
BAUDRATE = 9600

def send_signal_continuously(message, interval=1):
    """
    Gửi tín hiệu liên tục qua cổng serial với khoảng thời gian cố định.

    :param message: Chuỗi tín hiệu cần gửi
    :param interval: Khoảng thời gian giữa các lần gửi (giây)
    """
    ser = None  # Khởi tạo biến ser
    try:
        # Mở cổng serial
        ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")

        while True:
            # Gửi dữ liệu
            ser.write(message.encode())
            print(f"Sent: {message.strip()}")
            time.sleep(interval)  # Chờ trước khi gửi lần tiếp theo

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    # Chuỗi tín hiệu cần gửi
    message = "156697"  # Kết thúc bằng \n để tương thích với readline() bên nhận
    interval = 1  # Khoảng thời gian giữa các lần gửi (giây)
    send_signal_continuously(message, interval)


