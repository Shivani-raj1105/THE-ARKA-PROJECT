# Organic Botanist — Distributed AI Plant Detection Platform

A full-stack computer vision platform for plant identification built around an asynchronous inference pipeline using YOLOv8, FastAPI, Celery, Redis, and PostgreSQL.

The system demonstrates how modern ML services can decouple user-facing APIs from computationally expensive inference workloads while maintaining responsiveness, scalability, and persistent user history.

---

# Overview

Organic Botanist is an AI-powered plant identification platform designed to process uploaded images and return object detection results through an asynchronous backend architecture.

Rather than performing expensive model inference directly inside HTTP request handlers, the platform offloads computation to background workers using Celery and Redis. This enables responsive APIs while supporting concurrent inference workloads.

Key capabilities include:

* AI-based plant identification using YOLOv8
* Asynchronous inference pipeline
* User authentication
* Detection history
* Persistent task tracking
* Docker-based deployment
* Browser-based frontend

---

# System Architecture

```
Browser
   │
   ▼
FastAPI
   │
   ├── Authentication
   │
   ├── Image Upload
   │
   └── Task Creation
          │
          ▼
      Redis Broker
          │
          ▼
    Celery Worker
          │
          ▼
    YOLOv8 Inference
          │
          ▼
     PostgreSQL
          │
          ▼
     Detection History
          │
          ▼
      Browser Results
```

---

# Core Features

## AI Plant Detection

* YOLOv8 object detection
* Confidence scoring
* Multiple plant detection support
* Background inference

## Asynchronous Processing

* Non-blocking API responses
* Celery task queue
* Redis message broker
* Task polling

## User Management

* Registration
* Login
* Secure authentication
* Personal detection history

## Persistent Storage

* PostgreSQL backend
* User profiles
* Detection records
* Task state management

## Containerised Deployment

* Docker
* Docker Compose
* Shared storage volumes
* Service isolation

---

# Technology Stack

| Layer            | Technology                     |
| ---------------- | ------------------------------ |
| Backend          | FastAPI                        |
| ASGI             | Uvicorn                        |
| Task Queue       | Celery                         |
| Broker           | Redis                          |
| ML Model         | YOLOv8                         |
| Deep Learning    | PyTorch                        |
| Database         | PostgreSQL                     |
| Authentication   | Custom HMAC-SHA256             |
| Frontend         | HTML, Tailwind CSS, JavaScript |
| Containerisation | Docker                         |

---

# Detection Workflow

The inference pipeline follows an asynchronous execution model.

## Step 1

The user uploads an image.

```
POST /detect
```

---

## Step 2

FastAPI validates the request and stores the uploaded image.

---

## Step 3

A Celery task is created.

```
detect_plant_task.delay(...)
```

The API immediately returns:

```
{
    "task_id": "<uuid>"
}
```

---

## Step 4

The Celery worker:

* loads the YOLOv8 model,
* performs inference,
* generates predictions,
* stores results.

---

## Step 5

The frontend periodically polls:

```
GET /result/{task_id}
```

until completion.

---

## Step 6

Successful detections are displayed and optionally stored in the user's history.

---

# Authentication

Authentication is implemented without external JWT libraries.

Features include:

* HMAC-SHA256 signing
* Random password salts
* Seven-day token lifetime
* Bearer authentication
* Optional anonymous detections

Protected endpoints validate:

```
Authorization: Bearer <token>
```

---

# Database Design

Two primary entities drive the application.

## Users

Stores:

* account information,
* credentials,
* profile metadata.

## Plant Tasks

Stores:

* task IDs,
* user ownership,
* inference status,
* prediction outputs,
* timestamps.

Detection outputs are persisted as JSON structures for future retrieval.

---

# API Overview

## Authentication

```
POST /auth/register

POST /auth/login

GET /auth/me
```

---

## User

```
PUT /users/me

GET /users/me/history
```

---

## Detection

```
POST /detect

GET /result/{task_id}
```

---

# Frontend

The frontend is intentionally lightweight.

Built with:

* HTML
* Tailwind CSS
* Vanilla JavaScript
* ES Modules

Features:

* Login
* Registration
* Plant identification
* Detection history
* User profiles
* Automatic task polling

---

# Project Structure

```
app/

    main.py

    worker.py

    detection.py

    auth.py

    database.py

frontend_dist/

    login.html

    signup.html

    index.html

    history.html

    profile.html

    api.js

db_init/

Dockerfile

docker-compose.yml

requirements.txt
```

---

# Running Locally

## Requirements

* Docker Desktop

* YOLOv8 weights

---

Clone:

```bash
git clone <repository>
```

Build:

```bash
docker-compose up --build
```

Run:

```bash
docker-compose up
```

Open:

```
http://localhost:8000
```

---

# Current Capabilities

Implemented:

* FastAPI backend

* YOLOv8 integration

* Celery workers

* Redis broker

* PostgreSQL persistence

* User authentication

* Detection history

* Docker deployment

* Browser frontend

---

# Engineering Decisions

Several architectural choices were made to improve reliability.

## Background Workers

Inference is separated from HTTP requests to prevent blocking.

## Shared Volumes

Uploaded images are shared between API and worker containers without additional network transfer.

## Persistent Task Tracking

Task states are maintained independently of frontend sessions.

## Stateless APIs

Authentication tokens allow horizontal scaling.

---

# Future Work

Potential extensions include:

* WebSocket-based live updates

* Batch image processing

* Multi-model inference

* Mobile deployment

* Model versioning

* Explainable AI visualisations

* Distributed worker scaling

---

# Frontend

(Keep all existing screenshots exactly as they are.)

<img width="1894" height="904" alt="Screenshot 2026-05-01 195030" src="https://github.com/user-attachments/assets/bc59d18f-fa28-4752-aedb-8da848343e2d" />

<img width="1885" height="913" alt="Screenshot 2026-05-01 195125" src="https://github.com/user-attachments/assets/6c224aff-0c80-4828-b571-501be8812ea0" />

<img width="1886" height="893" alt="Screenshot 2026-05-01 195136" src="https://github.com/user-attachments/assets/a4512a71-7ad5-4b96-ae6e-00df21fce75a" />

<img width="1838" height="892" alt="Screenshot 2026-05-01 195151" src="https://github.com/user-attachments/assets/d26a5bbf-f198-4576-8823-c19ffb24bf71" />

---

# License

This project is intended for educational and research purposes.

MIT License.
now keep all this info , DO NOT CHANGE ANYTHING JUST ADD the iot part as well---

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
