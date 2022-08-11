import serial

serialport=serial.Serial('COM3', baudrate=9600, timeout=2)

for i in range(1,100):
    arduinodata=serialport.readline()
    print(arduinodata)