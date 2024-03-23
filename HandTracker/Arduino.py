import time
import requests
import serial


def tempCheck() :
    # Define your ThingSpeak API Key and Channel ID
    THINGSPEAK_API_KEY = "QDI5W438GL0XLB38"
    THINGSPEAK_CHANNEL_ID = "2281284"
    THINGSPEAK_URL = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"

    ser = serial.Serial('/dev/cu.usbserial-1140', 9600, timeout=1)
    time.sleep(2)
    ans = int()
    for i in range(5):
        line = ser.readline().decode("utf-8")
        humidity, temperature = float(line[2:6]), float(line[10:14])
        ans = temperature
        print(f"Humidity : {humidity} \nTemperature : {temperature}")
        response = requests.get(f"{THINGSPEAK_URL}&field1={temperature:.2f}&field2={humidity:.2f}")
        if response.status_code == 200:
            print("Data sent to ThingSpeak successfully")
        else:
            print("Failed to send data to ThingSpeak")
    return ans

if __name__ == '__main__' :
    print(f"Final : {tempCheck()}")