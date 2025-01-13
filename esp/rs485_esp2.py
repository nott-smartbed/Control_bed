from machine import Pin, UART
import uasyncio as asyncio
from utime import ticks_ms, ticks_diff

# Define motor states
REVERSE = 0
FORWARD = 1
BRAKE = 2

# Global variables
Up_max2 = 3000
Up_max3 = 3000
Up_max4 = 3000
first_time = False
start_state = False
pause_state = False
lean = 0
foot = 2000
head = 3000
prelean = 0
prehead = 0
prefoot = 0
bed_parameters = b""  # Đã là byte
old_forward_frame = b"FV"  # Đã là byte
old_bed_parameters = b"FV"  # Đã là byte

def Decode_frame(frame):
    global Up_max2, Up_max3, Up_max4, first_time, start_state, pause_state, head, lean, foot
    first_hash_index = frame.find(b'#')
    
    if first_hash_index == -1:
        raise ValueError("")
        # raise ValueError("Không tìm thấy dấu # trong chuỗi.")

    frame_part = frame[first_hash_index + 1:]
    parts = frame_part.split(b'|')

    if len(parts) < 7:
        raise ValueError("")
        # raise ValueError("Không có đủ 8 giá trị sau dấu #.")

    try:
        numbers = [int(part) for part in parts[:7]]
    except ValueError:
        # raise ValueError("Value is not number")
        raise ValueError("")

    return numbers

def combine_values(*values):
    return b"#" + b"|".join(map(str.encode, map(str, values)))

# UART Configuration
UART_ID = 1
BAUD_RATE = 9600
TX_PIN = 17
RX_PIN = 18
uart = UART(UART_ID, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, bits=8, parity=None, stop=1)

# Utility functions
def delay_ms(ms):
    receive_data()
    send_data()
    start_time = ticks_ms()
    while ticks_diff(ticks_ms(), start_time) < ms:
        pass

def send_data():
    global start_state, first_time, pause_state, prehead, prefoot, prelean, Up_max2, Up_max3, Up_max4, old_forward_frame
    forward_frame = combine_values(int(start_state), int(first_time), int(pause_state), prehead, prefoot, prelean, Up_max2, Up_max3, Up_max4)
    try:
        if old_forward_frame != forward_frame:
            uart.write(forward_frame)
            print(f"Sent: {forward_frame.decode('utf-8')}")
            old_forward_frame = forward_frame
    except Exception as e:
        print(f"UART send error: {e}")

def receive_data():
    global start_state, first_time, pause_state, head, foot, lean, sum_value, old_bed_parameters, bed_parameters, Up_max2, Up_max3, Up_max4

    try:
        if uart.any():
            data = uart.read()
            bed_parameters = Decode_frame(data)
            if bed_parameters != old_bed_parameters:
                print(f"Raw data received: {bed_parameters}")
                print(f"Before: bed_parameters: {bed_parameters},old_bed_parameters: {old_bed_parameters}")
                if len(bed_parameters) == 7:
                    (
                        start_state,
                        first_time,
                        pause_state,
                        head,
                        foot,
                        lean,
                        sum_value,
                    ) = bed_parameters

                    old_bed_parameters = bed_parameters
                    print(f"Decoded parameters: {bed_parameters}")
                    print(f"After: bed_parameters: {bed_parameters},old_bed_parameters: {old_bed_parameters}")
                    print(f"start: {start_state}, first_time: {first_time}, pause_state:{pause_state}, head: {head}, foot: {foot}, lean: {lean}\n")
                return bed_parameters
            else:
                return None

        return None
    except ValueError as ve:
        # print(f"Decode error: {ve}")
        return None
    except Exception as e:
        # print(f"UART receive error: {e}")
        return None

# Motor control
def control_motor(mode, enable_pin, motor_pin1, motor_pin2):
    try:
        receive_data()
        send_data()
        E_pin = Pin(enable_pin, Pin.OUT)
        mp1 = Pin(motor_pin1, Pin.OUT)
        mp2 = Pin(motor_pin2, Pin.OUT)
        
        if mode == REVERSE:
            E_pin.on()
            mp1.on()
            mp2.off()
        elif mode == FORWARD:
            E_pin.on()
            mp1.off()
            mp2.on()
        else:
            E_pin.off()
            mp1.off()
            mp2.off()
    except Exception as e:
        print(f"Motor control error: {e}")

# Motor-specific control functions
def DC1_CONTROL(mode):
    control_motor(mode, 37, 41, 47)

def DC2_CONTROL(mode):
    try:
        if mode == REVERSE and DC2_STATUS() == (1, 0):
            print("DC2 at minimum position.")
            mode = BRAKE
        if mode == FORWARD and DC2_STATUS() == (0, 1):
            print("DC2 at maximum position.")
            mode = BRAKE
        control_motor(mode, 38, 42, 48)
    except Exception as e:
        print(f"DC2 control error: {e}")

def DC3_CONTROL(mode):
    try:
        if mode == REVERSE and DC3_STATUS() == (1, 0, 0):
            print("DC3 at minimum position.")
            mode = BRAKE
        if mode == FORWARD and DC3_STATUS() == (0, 0, 1):
            print("DC3 at maximum position.")
            mode = BRAKE
        control_motor(mode, 39, 2, 35)
    except Exception as e:
        print(f"DC3 control error: {e}")

def DC4_CONTROL(mode):
    try:
        if mode == REVERSE and DC4_STATUS() == (1, 0, 0):
            print("DC4 at minimum position.")
            mode = BRAKE
        if mode == FORWARD and DC4_STATUS() == (0, 0, 1):
            print("DC4 at maximum position.")
            mode = BRAKE
        control_motor(mode, 40, 1, 36)
    except Exception as e:
        print(f"DC4 control error: {e}")

# Status checking
def DC2_STATUS():
    try:
        receive_data()
        send_data()
        I3 = Pin(19, Pin.IN, Pin.PULL_UP).value()
        I4 = Pin(4, Pin.IN, Pin.PULL_UP).value()
        return (I3, I4)
    except Exception as e:
        print(f"Error reading DC2 status: {e}")
        return (0, 0)

def DC3_STATUS():
    try:
        receive_data()
        send_data()
        I5 = Pin(5, Pin.IN, Pin.PULL_UP).value()
        I6 = Pin(6, Pin.IN, Pin.PULL_UP).value()
        I7 = Pin(7, Pin.IN, Pin.PULL_UP).value()
        return (I5, I6, I7)
    except Exception as e:
        print(f"Error reading DC3 status: {e}")
        return (0, 0, 0)

def DC4_STATUS():
    try:
        receive_data()
        send_data()
        I8 = Pin(15, Pin.IN, Pin.PULL_UP).value()
        I9 = Pin(16, Pin.IN, Pin.PULL_UP).value()
        I10 = Pin(8, Pin.IN, Pin.PULL_UP).value()
        return (I8, I9, I10)
    except Exception as e:
        print(f"Error reading DC4 status: {e}")
        return (0, 0, 0)

# Initialization and reset
def reset_all():
    print("Resetting all motors...")
    DC1_CONTROL(BRAKE)
    DC2_CONTROL(BRAKE)
    DC3_CONTROL(BRAKE)
    DC4_CONTROL(BRAKE)
    delay_ms(500)
    if not reset_lo():
        print("Reset failed. Retrying...")
        reset_lo()

def reset_lo():
    global prelean, prefoot, prehead
    
    print("Reseting...")
    
    if(DC4_STATUS() == (0, 1, 0)):
        while(DC2_STATUS() != (1, 0)):
            DC2_CONTROL(REVERSE)
        DC2_CONTROL(BRAKE)
        DC4_CONTROL(BRAKE)
        prelean = 0
        prehead = 0
        prefoot = 0
        print(f"prelean: {prelean}, prehead: {prehead}, prefoot: {prefoot}")
        print("Reset done!")
        return True
    
    elif (DC2_STATUS() == (1, 0)):
        while(DC4_STATUS() != (1, 0, 0)):
            DC4_CONTROL(REVERSE)
        DC4_CONTROL(BRAKE)
        print("DC4_STATUS: ", DC4_STATUS())
        delay_ms(1000)
        while(DC4_STATUS() != (0, 1, 0)):
            DC4_CONTROL(FORWARD)
        DC4_CONTROL(BRAKE)
        print("DC4_STATUS: ", DC4_STATUS())
        prelean = 0
        prehead = 0
        prefoot = 0
        print(f"prelean: {prelean}, prehead: {prehead}, prefoot: {prefoot}")
        print("Reset done!")
        return True
    else:
        print("Reset fail!")
        while True:
            if DC2_STATUS() == (1, 0) or DC4_STATUS() == (0, 1, 0):
                print("Correct value!")
                break
            DC4_CONTROL(BRAKE)
            DC2_CONTROL(BRAKE)
        
        return False

def Init_program():
    global Up_max2, Up_max3, Up_max4, first_time, head, prehead, foot, prefoot, lean, prelean
    
    print("Initializating...")
    DC1_CONTROL(2)
    DC2_CONTROL(2)
    DC3_CONTROL(2)
    DC4_CONTROL(2)
    delay_ms(500)
    
    if (DC2_STATUS() != (0, 1)) or (DC4_STATUS() != (0, 1, 0)):
        while(reset_lo() == False):
            reset_lo()
    print("Reset: ", reset_lo())
    print("Start get up max after 5s ...")
    
    for i in range(1, 6, 1):
        print(f"{i}s \n")
        delay_ms(1000)

    Up_max2 = 0
    time_up_2 = ticks_ms()
    while (DC2_STATUS() != (0, 1)):
        DC2_CONTROL(FORWARD)
    Up_max2 += (ticks_ms() - time_up_2)
    DC2_CONTROL(BRAKE)
    delay_ms(1000)
    while (DC2_STATUS() != (1, 0)):
        DC2_CONTROL(REVERSE)
    DC2_CONTROL(BRAKE)
    Up_max4 = 0
    time_up_4 = ticks_ms()
    delay_ms(1000)
    while (DC4_STATUS() != (0, 0, 1)):
        DC4_CONTROL(FORWARD)
    Up_max4 += (ticks_ms() - time_up_4)
    DC4_CONTROL(BRAKE)
    delay_ms(1000)
    while (DC4_STATUS() != (0, 1, 0)):
        DC4_CONTROL(REVERSE)
    DC4_CONTROL(BRAKE)
    if Up_max2 != 0 or Up_max3 != 0 or Up_max4 != 0:
        first_time = False
    receive_data()
    print(f"head: {head}, prehead: {prehead}, foot: {foot}, prefoot: {prefoot}, lean: {lean}, prelean:{prelean}")
    print(f"Up_max2: {Up_max2}, Up_max3: {Up_max3}, Up_max4: {Up_max4}")

def run_ver1():
    global prelean, prefoot, prehead, lean, foot, head
    print("...")
    print(f"head: {head}, prehead: {prehead}, lean: {lean}, prelean:{prelean}")
    print("Running...")
    if head == prehead and lean == prelean and foot == prefoot:
        pass
    else:
        if lean == 0:
            print("lean == 0")
            print("DC4 --> 0 1 0\n")
            while(DC4_STATUS() != (0, 1, 0)):
                if (prelean - lean < 0):
                    DC4_CONTROL(FORWARD)
                else:
                    DC4_CONTROL(REVERSE)

            DC4_CONTROL(BRAKE)
            prelean = 0
            print("check DC2")
            delay_ms(200)
            print("head: ", head)
            print("prehead: ", prehead)
            
            if (prehead - head < 0):
                delay_ms(1000)
                print("DC2_CONTROL(FORWARD)")
                time_FORWARD = abs(head - prehead)
                DC2_CONTROL(FORWARD)
                delay_ms(time_FORWARD)
                DC2_CONTROL(BRAKE)
            else:
                delay_ms(1000)
                print("DC2_CONTROL(REVERSE)")
                time_REVERSE = abs(head - prehead)
                DC2_CONTROL(REVERSE)
                delay_ms(time_REVERSE)
                DC2_CONTROL(BRAKE)

            prehead = head
            DC2_CONTROL(BRAKE)
            print(f"head: {head}, prehead: {prehead}, foot: {foot}, prefoot: {prefoot}, lean: {lean}, prelean:{prelean}")

        else:
            print("lean != 0\n")
            print(f"DC2 {prehead}--> 1 0\n")
            while(DC2_STATUS() != (1, 0)):
                if (prehead - head < 0):
                    DC2_CONTROL(FORWARD)
                else:
                    DC2_CONTROL(REVERSE)
                    
            DC2_CONTROL(BRAKE)
            prehead = 0
            prefoot = 0

            print(f"DC4 {prelean} --> {lean}\n")
            if (prelean - lean < 0):
                delay_ms(1000)
                print("DC4_CONTROL(FORWARD)")
                time_FORWARD = abs(prelean - lean)
                DC4_CONTROL(FORWARD)
                delay_ms(time_FORWARD)
            else:
                delay_ms(1000)
                print("DC4_CONTROL(REVERSE)")
                time_REVERSE = abs(prelean - lean)
                DC4_CONTROL(REVERSE)
                delay_ms(time_REVERSE)
            DC4_CONTROL(BRAKE)
            prelean = lean
            print(f"head: {head}, prehead: {prehead}, foot: {foot}, prefoot: {prefoot}, lean: {lean}, prelean:{prelean}")

# Main loop
while True:
    print("Starting main loop...")
    # while(DC2_STATUS() != (1, 0, 0)):
    #         DC2_CONTROL(REVERSE)
    # print(f"DC2: {DC2_STATUS()}")
    # print(f"DC4: {DC4_STATUS()}")
    print(start_state)
    delay_ms(500)
    while start_state:
        if first_time:
            print("Initializing...\n")
            Init_program()
            receive_data()
        print(f"Up_max2: {Up_max2}, Up_max3: {Up_max3}, Up_max4: {Up_max4}")
        print(f"head: {head}, prehead: {prehead} \n, foot: {foot}, prefoot: {prefoot} \n, lean: {lean}, prelean:{prelean}\n") 

        # Uncomment this section to enable data transmission and reception
        try:
            send_data()
            receive_data()
            for i in range(1,5,1):
                print(f"{i}s \n")
                delay_ms(1000)
            if prefoot != foot or prehead != head or prelean != lean:
                print("Run ver 1\n")
                run_ver1()
            print("\n\n Done!\n\n")
            DC1_CONTROL(2)
            DC2_CONTROL(2)
            DC3_CONTROL(2)
            DC4_CONTROL(2)
            send_data()
            receive_data()
        except KeyboardInterrupt:
            print("Exiting program...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")





