import time
import serial

def sendToArduino(data):
    try:
        ser = serial.Serial('/dev/cu.usbserial-1140', 9600, timeout=1)
        time.sleep(2)
        ser.write(data.encode())  # Send the data to the Arduino
        ser.close()  # Close the serial connection
        print(f"Data sent to Arduino: {data}")
    except Exception as e:
        print(f"Error sending data to Arduino: {str(e)}")

# Example of sending data to the Arduino
data_to_send = "Hello Arduino!"  # Replace with the data you want to send
sendToArduino(data_to_send)
