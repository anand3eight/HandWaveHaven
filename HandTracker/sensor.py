import time
import requests
import serial

def tempCheck(ser) :
    # Define your ThingSpeak API Key and Channel ID
    THINGSPEAK_API_KEY = "QDI5W438GL0XLB38"
    THINGSPEAK_CHANNEL_ID = "2281284"
    THINGSPEAK_URL = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"
    time.sleep(2)
    ans = int()
    ser.write(b'3')
    line = ser.readline().decode("utf-8")
    while True :
        try :
            humidity, temperature = float(line[2:6]), float(line[10:14])
            break
        except ValueError :
            line = ser.readline().decode("utf-8")
    if line is not None :
        humidity, temperature = float(line[2:6]), float(line[10:14])
        print(f"Humidity : {humidity} \nTemperature : {temperature}")
        response = requests.get(f"{THINGSPEAK_URL}&field1={temperature:.2f}&field2={humidity:.2f}")
        if response.status_code == 200:
            print("Data sent to ThingSpeak successfully")
        else:
            print("Failed to send data to ThingSpeak")
        return temperature
    else :
        return None

def buzzer(ser) :
    print('BUZZER')
    ser.write(b'2')
    print('Data Sent Successfully')

def led(ser) :
    print('LED')
    ser.write(b'1')
    print('Data sent successfully')

def off(ser) :
    print('OFF')
    ser.write(b'0')
    print('Data sent successfully')

if __name__ == '__main__' :
    # print(f"Final : {tempCheck()}")
    buzzer()