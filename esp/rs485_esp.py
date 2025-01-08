from machine import UART, Pin
import time

# Define UART parameters
UART_ID = 1
BAUD_RATE = 9600
TX_PIN = 17
RX_PIN = 18

# Initialize UART
uart = UART(UART_ID, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, bits=8, parity=None, stop=1)

def send_data(data):
    uart.write(data)
    print(f"Sent: {data}")

def receive_data():
    if uart.any():
        received_data = uart.read()
        return received_data
    return None

# Main loop
# try:
#     while True:
#         #Send data
#         send_data("1:ACK_LED_ON")
        
#         # Wait for a short period to allow for transmission
#         time.sleep(0.1)
        
#         # Check for received data
#         received = receive_data()
#         if received:
#             print(f"Received: {received}")
#         else:
#             print("No data received")
        
#         # Wait before next transmission
#         time.sleep(1)

# except KeyboardInterrupt:
#     print("Program terminated by user")

# finally:
#     # Close UART
#     uart.deinit()
#     print("UART closed")
