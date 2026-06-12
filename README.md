---

# IoT Integration Layer

In addition to the distributed AI inference platform, THE-ARKA-PROJECT incorporates an embedded IoT subsystem designed for real-world agricultural automation.

The hardware layer enables environmental sensing and autonomous irrigation control, complementing the software platform with physical actuation capabilities.

---

# IoT Architecture

```
Environmental Sensors
        │
        ▼
   Arduino Uno
        │
        ├── DHT11
        ├── Soil Moisture Sensor
        │
        ▼
 Decision Logic
        │
        ├── Relay Module
        ├── Water Pump
        ├── LCD Display
        └── Buzzer
```

---

# IoT Features

## Environmental Monitoring

The embedded subsystem continuously measures:

* Soil moisture
* Temperature
* Humidity

Sensor values are displayed locally and used for irrigation decisions.

---

## Automated Irrigation

The irrigation controller automatically activates a water pump based on soil moisture thresholds.

### Dry Soil

```
Moisture > 800
```

Water pump activates.

### Wet Soil

```
Moisture < 600
```

Water pump deactivates.

Relay behaviour can be configured through the relay logic settings.

---

## Local Monitoring

The integrated LCD provides live updates including:

* Temperature
* Humidity
* Soil moisture
* System status

The Serial Monitor outputs debugging information for development and diagnostics.

---

## Fault Detection

The system includes basic fault handling mechanisms.

Features include:

* DHT11 sensor validation
* Buzzer alerts on sensor failure
* Safe fallback behaviour

---

# Hardware Components

| Component            | Purpose                          |
| -------------------- | -------------------------------- |
| Arduino Uno          | Main controller                  |
| DHT11                | Temperature and humidity sensing |
| Soil Moisture Sensor | Soil condition monitoring        |
| Relay Module         | Pump switching                   |
| Water Pump           | Irrigation                       |
| I2C LCD              | Local display                    |
| Buzzer               | Fault notification               |

---

# Embedded Workflow

```
Read Sensors
      │
      ▼
Validate Inputs
      │
      ▼
Check Moisture Threshold
      │
      ▼
Control Relay
      │
      ▼
Update LCD
      │
      ▼
Repeat
```

---

# Arduino Setup

## Required Libraries

### DHT Sensor Library

Install:

* DHT sensor library by Adafruit
* Adafruit Unified Sensor

### LiquidCrystal_I2C

Install either:

* LiquidCrystal I2C by Frank de Brabander
* LiquidCrystal I2C by Marco Schwartz

---

## Arduino IDE Configuration

| Setting    | Value       |
| ---------- | ----------- |
| Board      | Arduino Uno |
| Programmer | AVRISP mkII |
| Baud Rate  | 9600        |

---

# Upload Procedure

1. Connect the Arduino Uno.
2. Open the project in Arduino IDE.
3. Verify the sketch.
4. Upload to the board.
5. Open the Serial Monitor at 9600 baud.

---

# Hardware Validation

| Feature        | Expected Behaviour              |
| -------------- | ------------------------------- |
| LCD            | Displays environmental readings |
| Water Pump     | Activates when soil is dry      |
| Relay          | Controls irrigation             |
| Buzzer         | Alerts on sensor failures       |
| Serial Monitor | Outputs diagnostic information  |

---

# Hybrid Architecture

THE-ARKA-PROJECT demonstrates the integration of two complementary engineering domains:

## Software Platform

* Distributed backend architecture
* AI-powered plant identification
* Asynchronous task execution
* Persistent user management

## Embedded IoT Layer

* Environmental sensing
* Automated irrigation
* Real-time hardware control
* Local monitoring and fault detection

Together, these components showcase an end-to-end cyber-physical system combining machine learning, distributed software, and embedded automation for sustainable agriculture.

---
