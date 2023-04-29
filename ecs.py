from machine import Pin,ADC
import time,utime
s1 = Pin(6,Pin.IN)
s2 = Pin(7,Pin.IN)
s3 = Pin(8,Pin.IN)
s4 = Pin(9,Pin.IN)
import machine
import utime
#lcd 
rs = machine.Pin(10,machine.Pin.OUT)
e = machine.Pin(11,machine.Pin.OUT)
d4 = machine.Pin(12,machine.Pin.OUT)
d5 = machine.Pin(13,machine.Pin.OUT)
d6 = machine.Pin(14,machine.Pin.OUT)
d7 = machine.Pin(15,machine.Pin.OUT)
 
def pulseE():
    e.value(1)
    utime.sleep_us(40)
    e.value(0)
    utime.sleep_us(40)
def send2LCD4(BinNum):
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
def send2LCD8(BinNum):
    d4.value((BinNum & 0b00010000) >>4)
    d5.value((BinNum & 0b00100000) >>5)
    d6.value((BinNum & 0b01000000) >>6)
    d7.value((BinNum & 0b10000000) >>7)
    pulseE()
    d4.value((BinNum & 0b00000001) >>0)
    d5.value((BinNum & 0b00000010) >>1)
    d6.value((BinNum & 0b00000100) >>2)
    d7.value((BinNum & 0b00001000) >>3)
    pulseE()
def setUpLCD():
    rs.value(0)
    send2LCD4(0b0011)
    send2LCD4(0b0011)
    send2LCD4(0b0011)
    send2LCD4(0b0010)
    send2LCD8(0b00101000)
    send2LCD8(0b00001100)
    send2LCD8(0b00000110)
    send2LCD8(0b00000001)
    utime.sleep_ms(2)
 

myHOST = 'api.thingspeak.com'
myPORT = '80'
myAPI = 'IYZT9FFNQ8871MR4' 


uart0 = machine.UART(1, baudrate=115200)
print(uart0)
second=0
def Rx_ESP_Data():
    recv=bytes()
    while uart0.any()>0:
        recv+=uart0.read(1)
    res=recv.decode('utf-8')
    return res
def Connect_WiFi(cmd, uart=uart0, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    utime.sleep(7.0)
    Wait_ESP_Rsp(uart, timeout)
    print()

def Send_AT_Cmd(cmd, uart=uart0, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    Wait_ESP_Rsp(uart, timeout)
    print()
    
def Wait_ESP_Rsp(uart=uart0, timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)


Send_AT_Cmd('AT\r\n')          
Send_AT_Cmd('AT+GMR\r\n')      
Send_AT_Cmd('AT+CIPSERVER=0\r\n')      
Send_AT_Cmd('AT+RST\r\n')     
Send_AT_Cmd('AT+RESTORE\r\n')  
Send_AT_Cmd('AT+CWMODE?\r\n')  
Send_AT_Cmd('AT+CWMODE=1\r\n') 
Send_AT_Cmd('AT+CWMODE?\r\n')  
Connect_WiFi('AT+CWJAP="Srujana","password"\r\n', timeout=5000) 
Send_AT_Cmd('AT+CIFSR\r\n',timeout=5000)    
Send_AT_Cmd('AT+CIPMUX=1\r\n')   
utime.sleep(1.0)
print ('Starting connection to ESP8266...')

while True:
    
    S1=1-s1.value()
    S2=1-s2.value()
    S3=1-s3.value()
    S4=1-s4.value()
    
    P="Full"
    F="Free"
    
    if (S1==1):
        S1=P
    else:
        S1=F
    
    if (S2==1):
        S2=P
    else:
        S2=F
    
    if (S3==1):
        S3=P
    else:
        S3=F

    if (S4==1):
        S4=P
    else:
        S4=F

    print("slot1:"+ str(S1) + " slot2:" + str(S2))
    print("slot3:"+ str(S3) + " slot4:" + str(S4))
    
    line1="S1:"+ str(S1) + " S2:" + str(S2)
    line2="S3:"+ str(S3) + " S4:" + str(S4)
    setUpLCD()
    rs.value(1)
    for x in line1:
        send2LCD8(ord(x))
        time.sleep(0.02)
    rs.value(0)
    time.sleep(0.02)
    send2LCD8(0b11000000)
    time.sleep(0.02)
    
    rs.value(1)
    for x in line2:
        send2LCD8(ord(x))
        time.sleep(0.02)

    time.sleep(1)
    second=second+1
    
    S1=1-s1.value()
    S2=1-s2.value()
    S3=1-s3.value()
    S4=1-s4.value()

    if(second==11):
        second=0
        sendData = 'GET /update?api_key='+ myAPI +'&field1='+str(S1) +'&field2='+str(S2) +'&field3='+str(S3) +'&field4='+str(S4)
        Send_AT_Cmd('AT+CIPSTART=0,\"TCP\",\"'+ myHOST +'\",'+ myPORT+'\r\n')
        utime.sleep(1.0)
        Send_AT_Cmd('AT+CIPSEND=0,' +str(len(sendData)+4) +'\r\n')
        utime.sleep(1.0)
        Send_AT_Cmd(sendData +'\r\n')
        utime.sleep(4.0)
        Send_AT_Cmd('AT+CIPCLOSE=0'+'\r\n') 
        utime.sleep(4.0)
        print ('Data sending to thing speak')