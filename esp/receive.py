import serial

# Cấu hình cổng USB-RS485
SERIAL_PORT = 'COM7'  # Thay đổi thành cổng COM phù hợp trên máy tính nhận
BAUDRATE = 9600

def receive_signal():
    ser = None
    try:
        # Mở cổng serial
        ser = serial.Serial(SERIAL_PORT, bytesize=8, baudrate=BAUDRATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")

        while True:
            # Đọc dữ liệu từ cổng serial
            data = ser.readline().decode('utf-8').strip()
            if data:
                print(f"Received: {data}")

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
    receive_signal()
