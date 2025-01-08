
from machine import Pin, PWM, UART
from utime import sleep, ticks_ms
from libT import delayT_ms



# State motor
reverse = 0
forward = 1
brake   = 2
#input user
lean = 0
foot = 2000 
head = 3000
prelean = 0
# prefoot =
prehead = 9952
#
Up_max2 = 3000
Up_max3 = 3000
Up_max4 = 3000
#
first_time = False
start_state = False
pause = False
RS485_state = False
# Define UART parameters
UART_ID = 1
BAUD_RATE = 9600
TX_PIN = 17
RX_PIN = 18

# Initialize UART
uart = UART(UART_ID, baudrate=BAUD_RATE, tx=TX_PIN, rx=RX_PIN, bits=8, parity=None, stop=1)

def delayT_ms(delay_ms):
    start_time = ticks_ms()
    while ticks_diff(ticks_ms(), start_time) < delay_ms:
        pass 

def send_data(data):
    uart.write(data)
    print(f"Sent: {data}")

def receive_data():
    if uart.any():
        received_data = uart.read()
        return received_data
    return None

def DC1_STATUS():
    print("Status DC1")
    I1_pin = Pin(21, Pin.IN, Pin.PULL_UP)  
    I2_pin = Pin(20, Pin.IN, Pin.PULL_UP)
    I1 = I1_pin.value()
    I2 = I2_pin.value()
    return I1,I2

def DC2_STATUS():
    #print("Status DC2")
    I3_pin = Pin(19, Pin.IN, Pin.PULL_UP)  
    I4_pin = Pin(4, Pin.IN, Pin.PULL_UP)  
    I3 = I3_pin.value()
    I4 = I4_pin.value()
    return I3,I4

def DC3_STATUS():
    # print("Status DC3")
    I5_pin = Pin(5, Pin.IN, Pin.PULL_UP) 
    I6_pin = Pin(6, Pin.IN, Pin.PULL_UP)  
    I7_pin = Pin(7, Pin.IN, Pin.PULL_UP)  
    I5 = I5_pin.value()
    I6 = I6_pin.value()
    I7 = I7_pin.value()
    return I5,I6,I7
    
def DC4_STATUS():
    #print("Status DC4")
    I8_pin = Pin(15, Pin.IN, Pin.PULL_UP)  
    I9_pin = Pin(16, Pin.IN, Pin.PULL_UP)  
    I10_pin = Pin(8, Pin.IN, Pin.PULL_UP) 
    I8 = I8_pin.value()
    I9 = I9_pin.value()
    I10 = I10_pin.value()
    return I8,I9,I10

def control_Motor(mode, enable_pin, motor_pin1, motor_pin2):
    E_pin = Pin(enable_pin, Pin.OUT)
    mp1 = Pin(motor_pin1, Pin.OUT)
    mp2 = Pin(motor_pin2, Pin.OUT)
    
    #mode == 0: forward | mode == 1: reverse | default = brake
    
    if mode == 0:
        #print("Reverting...")
        E_pin.on()
        mp1.on()
        mp2.off()
    elif mode == 1:
        #print("Forwarding ...")
        E_pin.on()
        mp1.off()
        mp2.on()
    else:
        #print("Braking ...")
        E_pin.off()
        mp1.off()
        mp2.off()

def DC1_CONTROL(mode):
    control_Motor(mode,37,41,47)
    
def DC2_CONTROL(mode):
    if mode == 0 :
        if DC2_STATUS() == (1,0):
            print("min DC2")
            mode = brake
    if mode == 1 :
        if  DC2_STATUS() == (0,1):
            print("Max DC2")
            mode = brake
    control_Motor(mode,38,42,48)
    
def DC3_CONTROL(mode):
    global paused
    if mode == 0 :
        if DC3_STATUS() == (1,0,0) :
            print("min DC3")
            mode = brake
    if mode == 1:
        if DC3_STATUS() == (0,0,1):
            print("Max DC3")
            mode = brake
    control_Motor(mode,39,2,35)
    
def DC4_CONTROL(mode):
    if mode == 0:
        if DC4_STATUS() == (1,0,0):
            print("min DC4")
            mode = brake
    if mode == 1:
        if DC4_STATUS() == (0,0,1):
            print("Max DC4")
            mode = brake
    control_Motor(mode,40,1,36) 

def reset_lo():
    global prelean,prefoot, prehead
    
    print("Reseting...")
    
    if(DC4_STATUS() == (0,1,0)):
        
        while(DC2_STATUS() != (1,0)):
            DC2_CONTROL(reverse)
        DC2_CONTROL(brake)
        DC4_CONTROL(brake)
        prelean = 0
        prehead = 0
        prefoot = 0
        print(f"prelean: {prelean}, prehead: {prehead}, prefoot: {prefoot}")
        print("Reset done!")
        return True
    
    elif (DC2_STATUS() == (1,0)):
        while(DC4_STATUS() != (1,0,0)):
            DC4_CONTROL(reverse)
        DC4_CONTROL(brake)
        print("DC4_STATUS: ",DC4_STATUS())
        delayT_ms(1000)
        while(DC4_STATUS() != (0,1,0)):
            DC4_CONTROL(forward)
        DC4_CONTROL(brake)
        print("DC4_STATUS: ",DC4_STATUS())
        prelean = 0
        prehead = 0
        prefoot = 0
        print(f"prelean: {prelean}, prehead: {prehead}, prefoot: {prefoot}")
        print("Reset done!")
        return True
    else:
        while True:
            if DC2_STATUS() == (1,0) or DC4_STATUS() == (0,1,0):
                print("Correct value!")
                break
            DC4_CONTROL(brake)
            DC2_CONTROL(brake)
        print("Reset fail!")
        return False
            
    

def Init_program():
    global paused
    global Up_max2, Up_max3, Up_max3
    
    print("Initializating...")
    DC1_CONTROL(2)
    DC2_CONTROL(2)
    DC4_CONTROL(2)
    DC4_CONTROL(2)
    delayT_ms(500)
    
    if (DC2_STATUS() != (0,1)) or (DC4_STATUS() != (0,1,0)):
        while(reset_lo()==False):
            reset_lo()
    print("Reset: ",reset_lo())

    Up_max2 = 0
    time_up_2 = ticks_ms()
    while (DC2_STATUS() != (0,1)):
        DC2_CONTROL(forward)
    Up_max2 += (ticks_ms() - time_up_2)
    DC2_CONTROL(brake)
    delayT_ms(1000)
    while (DC2_STATUS() != (1,0)):
        DC2_CONTROL(reverse)
    DC2_CONTROL(brake)
        
    Up_max3 = 0
    time_up_3 = ticks_ms()
    while (DC4_STATUS() != (0,0,1)):
        DC4_CONTROL(forward)
    Up_max3 += (ticks_ms() - time_up_3)
    DC4_CONTROL(brake)
    delayT_ms(1000)
    while (DC4_STATUS() != (0,1,0)):
        DC4_CONTROL(reverse)
    DC4_CONTROL(brake)
    print(f"Up_max2: {Up_max2}, Up_max3: {Up_max3}, Up_max3: {Up_max3}")


#----------------------- run ----------------
def run_ver1():
    # global paused
    global prelean, prefoot, prehead, lean, foot, head
    print("Start...")
    # if (DC2_STATUS() != (0,1)) or (DC4_STATUS() != (0,1,0)):
    #     while(reset_lo()==False):
    #         reset_lo()
    #print("Reset: ",reset_lo())
    print(f"head: {head}, prehead: {prehead}, lean: {lean}, prelean:{prelean}")
    print("Running...")

    if head == prehead and lean == prelean:
        pass
    else:
        if lean == 0:
            print("lean == 0")

            print("DC4 --> 0 1 0\n")
            while(DC4_STATUS() != (0,1,0)):
                if (prelean - lean < 0):
                    # delayT_ms(1000)
                    # print("DC4_CONTROL(forward)")
                    # time_forward = abs(prelean - lean)
                    # while(DC4_STATUS() != (0,1,0)):
                    DC4_CONTROL(forward)
                    # prelean += (ticks_ms() - time_up_3)
                    # print("lean - prelean",lean-prelean)
                else:
                    # delayT_ms(1000)
                    # print("DC4_CONTROL(reverse)")
                    # time_down_3 = ticks_ms()
                    # while(DC4_STATUS() != (0,1,0)):
                    DC4_CONTROL(reverse)
                    # prelean -= (ticks_ms() - time_down_3)
                    # print("lean - prelean",lean-prelean)

            DC4_CONTROL(brake)
            prelean = 0

            print("check DC2")
            delayT_ms(200)
            print("head: ",head)
            print("prehead: ",prehead)
            
            if (prehead - head < 0):
                delayT_ms(1000)
                print("DC2_CONTROL(forward)")
                time_forward = abs(head - prehead)
                DC2_CONTROL(forward)
                delayT_ms(time_forward)
                DC2_CONTROL(brake)
            else:
                delayT_ms(1000)
                print("DC2_CONTROL(reverse)")
                time_reverse = abs(abs(head - prehead))
                DC2_CONTROL(reverse)
                delayT_ms(time_reverse)
                DC2_CONTROL(brake)

            prehead = head
            DC2_CONTROL(brake)
            print(f"head: {head}, prehead: {prehead}, lean: {lean}, prelean:{prelean}")
            print("Done DC2")

        
        else:
            print("lean != 0") # vi vậy head = foot = 0 --> 

            while(DC2_STATUS() != (1,0)):
                if (prehead - head < 0):
                    # delayT_ms(1000)
                    DC2_CONTROL(forward)
                else:
                    # delayT_ms(1000)
                    DC2_CONTROL(reverse)
                    
            DC2_CONTROL(brake)
            prehead = 0

            prefoot = 0
            if (prelean - lean < 0):
                delayT_ms(1000)
                print("DC4_CONTROL(forward)")
                time_forward = abs(prelean - lean)
                DC4_CONTROL(forward)
                delayT_ms(time_forward)
            else:
                delayT_ms(1000)
                print("DC4_CONTROL(reverse)")
                time_reverse = abs(prelean - lean)
                DC4_CONTROL(reverse)
                delayT_ms(time_reverse)
            DC4_CONTROL(brake)
            print(f"head: {head}, prehead: {prehead}, foot: {foot}, prefoot: {prefoot}, lean: {lean}, prelean:{prelean}")

    
print("Stop all!\n")
DC1_CONTROL(2)
DC2_CONTROL(2)
DC3_CONTROL(2)
DC4_CONTROL(2)
delayT_ms(500)
while(reset_lo()==False):
    pass
while True:
    #
    #print(DC4_STATUS())
    # print(DC1_STATUS())
    # print(DC2_STATUS())
    # print(DC3_STATUS())
    # print(DC4_STATUS())
    # delayT_ms(1000)
    # if first_time:
    #     Init_program()
    # print("Bat dau chay chuong trinh\n")
    # run_ver1()
    # print("ket thuc chuong trinh")
    delayT_ms(1000)







