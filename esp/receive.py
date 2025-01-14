import serial

# Cấu hình cổng USB-RS485
SERIAL_PORT = 'COM7'  # Thay đổi thành cổng COM của bạn
BAUDRATE = 9600

def receive_signal_continuously():
    """
    Nhận tín hiệu liên tục từ cổng serial và hiển thị lên màn hình.
    """
    ser = None  # Khởi tạo biến ser
    try:
        # Mở cổng serial
        ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")
        
        while True:
            # Đọc dữ liệu từ cổng serial
            if ser.in_waiting > 0:  # Kiểm tra nếu có dữ liệu chờ đọc
                data = ser.readline().decode().strip()  # Đọc một dòng và giải mã
                print(f"Received: {data}")  # Hiển thị dữ liệu nhận được

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
    receive_signal_continuously()
