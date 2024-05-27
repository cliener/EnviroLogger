from sense_hat import SenseHat
from datetime import datetime
import csv_log, logging, time

sense = SenseHat()
sense.set_rotation(180)
#sense.color.gain = 60
#sense.color.integration_cycles = 64

# delay in seconds
delay_display = 10
# Display delay x log count multiplier
# Logs once every delay_log runs of display
delay_log = 6

# Compile sense data
def get_sense_data():
    sense_data = {}
    
    # Get environment data
    sense_data["temp"] = sense.get_temperature()
    sense_data["pres"] = sense.get_pressure()
    sense_data["hum"] = sense.get_humidity()
    
    # We're not logging this data
    # Get orientation data
    # orientation = sense.get_orientation()
    # sense_data["yaw"] = orientation["yaw"]
    # sense_data["pitch"] = orientation["pitch"]
    # sense_data["roll"] = orientation["roll"]
    
    # Get compass data
    # mag = sense.get_compass_raw()
    # sense_data["mag_x"] = mag["x"]
    # sense_data["mag_y"] = mag["y"]
    # sense_data["mag_z"] = mag["z"]
    
    # Get accelerometer data
    # acc = sense.get_accelerometer_raw()
    # sense_data["acc_x"] = acc["x"]
    # sense_data["acc_y"] = acc["y"]
    # sense_data["acc_z"] = acc["z"]
    
    # Get gyroscope data
    # gyro = sense.get_gyroscope_raw()
    # sense_data["gyro_x"] = gyro["x"]
    # sense_data["gyro_y"] = gyro["y"]
    # sense_data["gyro_z"] = gyro["z"]
    
    # sense_data["datetime"] = datetime.now()
    sense_data["datetime"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

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

# CSV Logger
# Create logger with csv rotating handler
LOG_HEADER = ['temp', 'pres', 'hum', 'datetime'] # Pass None for no csv header

# Record and show stats
logger = csv_log.RotatingCsvLogger(logging.INFO, csv_log.LOG_FORMAT, csv_log.LOG_DATE_FORMAT,
        csv_log.LOG_FILE_NAME, csv_log.LOG_MAX_SIZE, csv_log.LOG_MAX_FILES, LOG_HEADER)

display_count = 0
show_data = False

timestamp = time.perf_counter()

while True:
    now = time.perf_counter()
    time_difference = now - timestamp
    seconds = int(time_difference)

    # Capture joystick event
    event = sense.stick.wait_for_event(emptybuffer = True)

    # Trigger display when the joystick is pressed
    if event.action == "pressed":
        show_data = True

    # Every delay seconds
    if seconds % delay_display == 0:
        data = get_sense_data()
        # Update count
        display_count = display_count + 1
        time.sleep(1)

        # Log data
        if (display_count == delay_log):
            # Reset count
            display_count = 0
            # Write to CSV
            logger.info(data)
            # Reset timer
            timestamp = time.perf_counter()

        # Update display when triggered
        if show_data:
           show_sense_data(data)
           show_data = False
