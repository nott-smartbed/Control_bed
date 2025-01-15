import serial
import time

# Cấu hình cổng USB-RS485
SERIAL_PORT = 'COM6'  # Thay đổi thành cổng COM của bạn
BAUDRATE = 9600

def send_signal_continuously(message, interval=1):
    """
    Gửi tín hiệu liên tục qua cổng serial với khoảng thời gian cố định.

    Args:
        message (str): Chuỗi tín hiệu cần gửi.
        interval (float): Khoảng thời gian giữa các lần gửi (tính bằng giây).
    """
    try:
        # Mở cổng serial
        with serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")

            while True:
                # Gửi dữ liệu
                # ser.write(message.encode('utf-8'))
                ser.write(message.encode())
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sent: {message.strip()}")
                time.sleep(interval)  # Chờ trước khi gửi lần tiếp theo

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Program terminated.")

if __name__ == "__main__":
    # Chuỗi tín hiệu cần gửi
    message = "['69.0', '0.0', '0.0', 'off', 'off', 'off', 'off', 'off', 'off', 'on', 'off']"  # Kết thúc bằng \n để tương thích với readline() bên nhận
    interval = 0.2  # Khoảng thời gian giữa các lần gửi (giây)
    send_signal_continuously(message, interval)
