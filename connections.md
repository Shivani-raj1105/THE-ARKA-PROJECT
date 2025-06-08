# 🌿 Smart Solar-Powered Irrigation System

An automated, eco-friendly irrigation system powered by solar energy. It intelligently monitors soil moisture and environmental conditions to water plants only when necessary — saving water and reducing manual effort.

---

## 🔧 Components Used

- ☀️ **Solar Panel** – Generates renewable energy to power the system  
- 🌡️ **DHT11 Sensor** – Measures temperature and humidity  
- 🔊 **Buzzer** – Sounds an alert when soil is dry  
- 🧠 **Arduino UNO R3** – Central controller for sensors and actuators  
- 🔌 **Breadboard** – Used to prototype circuit connections  
- 🔗 **Jumper Wires** – Connect components and modules  
- 📺 **LCD Display (I2C)** – Shows sensor data in real-time  
- ⚡ **Relay Module** – Controls power to the water pump  
- 🔋 **Rechargeable Batteries** – Stores energy from the solar panel  
- 🌱 **Soil Moisture Sensor** – Detects soil moisture level  
- 🪴 **Soil** – The growth medium for plants  
- 🚿 **Water Pipes** – Direct water to the soil  
- 💧 **Water Pump** – Pumps water when soil is dry

---

## ⚙️ Circuit Connections

### 🌡️ **DHT11 Sensor**
- `VCC` → 5V  
- `GND` → GND  
- `Data` → D4

### 🔊 **Buzzer**
- `+` → D7  
- `-` → GND

### 🌱 **Soil Moisture Sensor**
- `Brown` (GND) → GND  
- `Red` (VCC) → 5V  
- `Yellow` (Signal) → A0

### ⚡ **Relay Module**
- `VCC` → 5V  
- `GND` → GND  
- `IN` → D8  
- `COM` → Battery Positive (BP)  
- `NO` (Normally Open) → Water Pump Positive

### 💧 **Water Pump**
- `Positive` → Relay NO  
- `Negative` → Battery Negative (BN)

### ☀️ **Solar Panel**
- `Positive` → Battery Positive  
- `Negative` → Battery Negative

### 📺 **LCD Display (I2C)**
- `VCC` → 5V  
- `GND` → GND  
- `SDA` → A4  
- `SCL` → A5

---

## 📌 Notes

- Use a common ground (GND) across all components  
- Include a diode across the pump if needed for back EMF protection  
- A voltage regulator is recommended if your solar panel provides >5V  
- Keep wires tidy and connections secure for stability  

---

Our circuit looked somewhat like this:
![Smart Irrigation Circuit Diagram](https://github-production-user-asset-6210df.s3.amazonaws.com/190762103/452787386-2c302532-7b01-455c-82ba-f0942d54cc3d.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250608%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250608T125833Z&X-Amz-Expires=300&X-Amz-Signature=2cab874ce51908ddbff6f6106ff0b0c45248d4d49043de767b1ba4981e875a2b&X-Amz-SignedHeaders=host)

