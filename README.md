# THE-ARKA-PROJECT
You need to install these libraries from the Arduino Library Manager:

DHT sensor library

Go to Sketch → Include Library → Manage Libraries...

Search for DHT sensor library by Adafruit

Install it

Also install Adafruit Unified Sensor if prompted

LiquidCrystal_I2C

Search for LiquidCrystal_I2C in Library Manager

Install LiquidCrystal I2C by Frank de Brabander or by Marco Schwartz
 4. Arduino IDE Settings
Board: Select Arduino Uno under Tools → Board

Port: Select the correct COM port under Tools → Port

Programmer: Default AVRISP mkII
Connect Arduino to your PC via USB.

Open the code in Arduino IDE.

Click ✅ "Verify" (Compile the code).

Click → "Upload" (Transfer code to board).

Open Serial Monitor (Tools → Serial Monitor) at 9600 baud rate to view logs.
What to check:
LCD shows temperature, humidity, and soil moisture values.

Buzzer sounds if DHT11 fails.

Pump turns ON when soil is dry (value > 800).

Pump turns OFF when soil is wet (value < 600).

Relay behavior matches your RELAY_ACTIVE_HIGH setting.
