CREATE TABLE envirolog(id INTEGER PRIMARY KEY AUTOINCREMENT, temperature REAL, humidity REAL, pressure REAL, date DATETIME);

INSERT INTO envirolog (temperature, humidity, pressure, date)
VALUES (, , , datetime("now"));

SELECT temperature, humidity, pressure, date
FROM envirolog
ORDER BY date DESC