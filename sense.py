from sense_hat import SenseHat
from datetime import datetime
from csv import writer
import sys
from random import randint

sense = SenseHat()
#sense.color.gain = 60
#sense.color.integration_cycles = 64

timestamp = datetime.now()
# delay in seconds
delay_display = 15
delay_log = 60

# Compile sense data
def get_sense_data():
    sense_data = []
    
    # Get environment data
    sense_data.append(sense.get_temperature())
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())
    
    # Get orientation data
    orientation = sense.get_orientation()
    sense_data.append(orientation["yaw"])
    sense_data.append(orientation["pitch"])
    sense_data.append(orientation["roll"])
    
    # Get compass data
    mag = sense.get_compass_raw()
    sense_data.append(mag["x"])
    sense_data.append(mag["y"])
    sense_data.append(mag["z"])
    
    # Get accelerometer data
    acc = sense.get_accelerometer_raw()
    sense_data.append(acc["x"])
    sense_data.append(acc["y"])
    sense_data.append(acc["z"])
    
    # Get gyroscope data
    gyro = sense.get_gyroscope_raw()
    sense_data.append(gyro["x"])
    sense_data.append(gyro["y"])
    sense_data.append(gyro["z"])
    
    sense_data.append(datetime.now())

    return sense_data

# Display 
white = (128, 128, 128)
red = (128,0,0)
blue = (0,0,128)
off = (0,0,0)
scroll = 0.05

def humidity():
    sense.show_message("H: "+str(round(sense.humidity,1))+"%", text_colour=white, back_colour=off, scroll_speed=scroll)
    
def pressure():
    sense.show_message("P: "+str(round(sense.pressure,2))+" M", text_colour=red, back_colour=off, scroll_speed=scroll)
    
def temp():
    sense.show_message("T: "+str(round(sense.get_temperature(),1))+"C", text_colour=blue, back_colour=off, scroll_speed=scroll)

# Show all environment data
def show_sense_data():
    humidity()
    pressure()
    temp()

# Record and show stats
with open('data.csv', 'w', buffering=1, newline='') as f:
    # Init CSV header
    data_writer = writer(f)
    data_writer.writerow(['temp', 'pres', 'hum',
                           'yaw', 'pitch', 'roll',
                           'mag_x', 'mag_y', 'mag_z',
                           'acc_x', 'acc_y', 'acc_z'
                           'gyro_x', 'gyro_y', 'gyro_z',
                           'datetime'])
    
    while True:
        data = get_sense_data()
        time_difference = data[-1] - timestamp
        seconds = time_difference.seconds
        # Every delay seconds
 #       if time_difference.seconds > delay_display:
            # Write to CSV
#            data_writer.writerow(data)
        # Every delay seconds
        if seconds % delay_display == 1:
        # if seconds - delay_display == 1:
        # if time_difference.seconds > delay_display:
            print(seconds)
            print(seconds / delay_display)
            print((seconds - 1) % delay_display == 0)
            print(seconds - delay_display == 1)
            # Update display
            show_sense_data()
            if seconds - delay_display == 1:
                timestamp = datetime.now()


    
def outski():
    print("quitting")
    sys.exit()

sense.stick.direction_up = humidity
sense.stick.direction_down = outski
sense.stick.direction_left = pressure
sense.stick.direction_right = temp

while True:
    pass    

