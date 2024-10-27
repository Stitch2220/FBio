
import serial

# Replace "port_name" with the appropriate port name
serial_port = "COM4"
baud_rate = 500000

# Establish a connection to the serial port:
arduino = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:

        # Read data from the serial port
        data_str = arduino.readline().decode('utf-8').strip()

        # If data received, print it
        if data_str:
            timestamp, data = map(float, data_str.split(","))
            print(f"timestamp: {timestamp} | data: {data}")

# To close the serial port gracefully, use Ctrl+C to break the loop
except KeyboardInterrupt:
    print("KeyboardInterrupt")

except Exception as e:
    print(f"Closing the serial port due to {e}.")

finally:
    arduino.close()
    print("Serial port closed")

