from sense_hat import SenseHat
from datetime import datetime
import csv_log, logging, sqlite3, threading, time

sense = SenseHat()
#sense.color.gain = 60
#sense.color.integration_cycles = 64

# Delay in seconds
delay_log = 60

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
    # clear the screen
    sense.clear()
    time.sleep(1)

    # temp
    sense.show_message(f"T: {data['temp']:.1f}C", text_colour=blue, back_colour=off, scroll_speed=scroll)

    # humidity
    sense.show_message(f"H: {data['hum']:.1f}%", text_colour=white, back_colour=off, scroll_speed=scroll)
    
    # pressure
    sense.show_message(f"P: {data['pres']:.2f} M", text_colour=red, back_colour=off, scroll_speed=scroll)

def log_to_db(data):
    con = sqlite3.connect("../../piloggerSQLite.db")
    cur = con.cursor()
    cur.execute("""
INSERT INTO envirolog (temperature, humidity, pressure, date)
VALUES (?, ?, ?, datetime("now"));
                """, (data['temp'], data['hum'], data['pres'],))
    con.commit()
    con.close()

# Separate thread to watch joystick presses
def joystick_watch():
    while True:
        event = sense.stick.wait_for_event(emptybuffer = True)

        # Trigger display when the joystick is pressed
        if event.action == "pressed":
            show_sense_data(get_sense_data())


# CSV Logger
# Create logger with csv rotating handler
LOG_HEADER = ['temp', 'pres', 'hum', 'datetime'] # Pass None for no csv header

# Launch joystick thread
x = threading.Thread(target=joystick_watch)
x.start()

# Record and show stats
logger = csv_log.RotatingCsvLogger(logging.INFO, csv_log.LOG_FORMAT, csv_log.LOG_DATE_FORMAT,
        csv_log.LOG_FILE_NAME, csv_log.LOG_MAX_SIZE, csv_log.LOG_MAX_FILES, LOG_HEADER)

# Log data every delay_log seconds
while True:
    # fetch data
    data = get_sense_data()

    # Write to DB
    log_to_db(data)

    # Write to CSV
    logger.info(data)

    # Delay
    time.sleep(delay_log)
