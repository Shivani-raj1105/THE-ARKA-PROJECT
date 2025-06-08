# How to run this :

## 📚 Required Libraries

To run this project successfully, install the following libraries in the **Arduino IDE**:

### ✅ DHT Sensor Library
- Go to `Sketch → Include Library → Manage Libraries...`
- Search for: **DHT sensor library by Adafruit**
- Click **Install**
- Also install: **Adafruit Unified Sensor** (if prompted)

### ✅ LiquidCrystal_I2C
- Search: `LiquidCrystal_I2C`
- Install: **LiquidCrystal I2C by Frank de Brabander** or **by Marco Schwartz**

---

## ⚙️ Arduino IDE Setup

### 🔧 Configuration
| Setting      | Value            |
|--------------|------------------|
| **Board**     | Arduino Uno       |
| **Port**      | Select your COM port |
| **Programmer**| AVRISP mkII       |

---

## 🔌 Uploading the Code

1. Connect your Arduino Uno to your PC via USB.
2. Open the `.ino` file in Arduino IDE.
3. Click ✅ **Verify** to compile the code.
4. Click ⬆️ **Upload** to flash the board.
5. Open **Serial Monitor** via `Tools → Serial Monitor` at **9600 baud**.

---

## ✅ What to Test

Once the system is powered and running:

| Feature             | Behavior                             |
|---------------------|--------------------------------------|
| 🖥️ **LCD Display**     | Shows temperature, humidity, and soil moisture |
| 🔊 **Buzzer**         | Alerts when the DHT11 sensor fails |
| 🚿 **Water Pump**      | Turns **ON** when soil is **dry** (moisture > 800) |
| 💧 **Pump Stops**      | Turns **OFF** when soil is **wet** (moisture < 600) |
| ⚡ **Relay Logic**     | Behavior aligns with `RELAY_ACTIVE_HIGH` flag |

---

🌱 *Built with a vision to empower sustainable farming through technology.*
