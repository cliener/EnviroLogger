from sense_hat import SenseHat
from datetime import datetime
from csv import writer
import csv
import sys
from random import randint

sense = SenseHat()
#sense.color.gain = 60
#sense.color.integration_cycles = 64

timestamp = datetime.now()
# delay in seconds
delay_display = 15
# Display delay x log count multiplier
# Logs once every delay_log runs of display
delay_log = 4

# Compile sense data
def get_sense_data():
    sense_data = {}
    
    # Get environment data
    sense_data["temp"] = sense.get_temperature()
    sense_data["pres"] = sense.get_pressure()
    sense_data["hum"] = sense.get_humidity()
    
    # Get orientation data
    orientation = sense.get_orientation()
    sense_data["yaw"] = orientation["yaw"]
    sense_data["pitch"] = orientation["pitch"]
    sense_data["roll"] = orientation["roll"]
    
    # Get compass data
    mag = sense.get_compass_raw()
    sense_data["mag_x"] = mag["x"]
    sense_data["mag_y"] = mag["y"]
    sense_data["mag_z"] = mag["z"]
    
    # Get accelerometer data
    acc = sense.get_accelerometer_raw()
    sense_data["acc_x"] = acc["x"]
    sense_data["acc_y"] = acc["y"]
    sense_data["acc_z"] = acc["z"]
    
    # Get gyroscope data
    gyro = sense.get_gyroscope_raw()
    sense_data["gyro_x"] = gyro["x"]
    sense_data["gyro_y"] = gyro["y"]
    sense_data["gyro_z"] = gyro["z"]
    
    sense_data["datetime"] = datetime.now()

    return sense_data

# Display 
white = (128, 128, 128)
red = (128,0,0)
blue = (0,0,128)
off = (0,0,0)
scroll = 0.05

# Show all environment data
def show_sense_data(data):    
    # temp
    sense.show_message(f"T: {data['temp']:.1f}C", text_colour=blue, back_colour=off, scroll_speed=scroll)

    # humidity
    sense.show_message(f"H: {data['hum']:.1f}%", text_colour=white, back_colour=off, scroll_speed=scroll)
    
    # pressure
    sense.show_message(f"P: {data['pres']:.2f} M", text_colour=red, back_colour=off, scroll_speed=scroll)

# Record and show stats
with open('data.csv', 'w', buffering=1, newline='') as csvFile:
    display_count = 0
    # Init CSV header
    data_writer = csv.DictWriter(csvFile, ['temp', 'pres', 'hum',
                           'yaw', 'pitch', 'roll',
                           'mag_x', 'mag_y', 'mag_z',
                           'acc_x', 'acc_y', 'acc_z',
                           'gyro_x', 'gyro_y', 'gyro_z',
                           'datetime'])
    data_writer.writeheader()
    
    while True:
        data = get_sense_data()
        time_difference = data["datetime"] - timestamp
        seconds = time_difference.seconds

        # Every delay seconds
        if seconds % delay_display == 1:
            # Update count
            display_count = display_count + 1

            if (display_count == delay_log):
                # Write to CSV
                data_writer.writerow(data)
                display_count = 0

            # Update display
            show_sense_data(data)

            # Reset timer
            if seconds - delay_display == 1:
                timestamp = datetime.now()
