<div align="center">

# ◉ Hybrid IDS — Real-Time Intrusion Detection System

**A full-stack, AI-powered network intrusion detection system combining rule-based heuristics and machine learning to detect, alert, and block malicious traffic in real time.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)

![Dashboard Preview](https://img.shields.io/badge/Status-Active-22c55e?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Training the ML Model](#-training-the-ml-model)
- [Running the Application](#-running-the-application)
- [Attack Simulations](#-attack-simulations)
- [API Reference](#-api-reference)
- [Database Schema](#-database-schema)
- [How Detection Works](#-how-detection-works)
- [Configuration](#-configuration)

---

## 🔍 Overview

Hybrid IDS is a network intrusion detection system that passively sniffs live network traffic and analyzes each packet through two parallel detection engines:

1. **Rule Engine** — Detects known attack patterns (port scans, brute force, DoS floods) using sliding-window heuristics with configurable thresholds.
2. **ML Engine** — Uses a Random Forest classifier trained on the [UNSW-NB15 dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset) to detect anomalous traffic with a confidence score.

When either engine fires, the source IP is automatically blocked and an alert is recorded. A live React dashboard streams all detections in real time via polling.

---

## ✨ Features

| Feature                      | Description                                                               |
| ---------------------------- | ------------------------------------------------------------------------- |
| 🔴 **Live Packet Capture**   | Sniffs raw network traffic using Scapy on all interfaces                  |
| 🧠 **ML Anomaly Detection**  | Random Forest model trained on UNSW-NB15 (~175k samples, 10 features)     |
| 📏 **Rule-Based Detection**  | Detects Port Scans, Brute Force, and DoS attacks via sliding time windows |
| 🚫 **Auto IP Blocking**      | Malicious IPs are instantly inserted into a `blocked_ips` table           |
| 📊 **Live Dashboard**        | React UI with traffic chart, attack pie chart, alert feed, and top IPs    |
| 🧪 **Attack Simulators**     | Three Scapy-based scripts to simulate real attacks for testing            |
| 🔌 **REST API**              | Full FastAPI backend with 8 endpoints for alerts, stats, and IPs          |
| 🗄️ **PostgreSQL Storage**    | All packets, alerts, blocked IPs, and traffic stats persisted to DB       |
| ⚡ **Threaded Architecture** | Sniffer, traffic rate recorder, and API server run concurrently           |
| 🔄 **Auto-Polling Frontend** | Dashboard auto-refreshes every 2–5 seconds without page reload            |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Network Traffic                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ Raw Packets
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Scapy Packet Sniffer                      │
│              capture/sniffer.py + feature_extractor.py       │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────┐    ┌─────────────────────────────────┐
│   Rule Engine        │    │         ML Engine                │
│ detection/rule_      │    │   detection/ml_engine.py         │
│ engine.py            │    │   Random Forest (UNSW-NB15)      │
│                      │    │   Confidence threshold: 0.75     │
│ • Port Scan          │    └──────────────┬──────────────────┘
│ • Brute Force        │                   │
│ • DoS Attack         │                   │
└──────────┬───────────┘                   │
           │                               │
           └──────────────┬────────────────┘
                          │ insert_alert() + block_ip()
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     PostgreSQL Database                      │
│   packets | alerts | blocked_ips | traffic_stats             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI REST API  (port 8000)                   │
│   /api/alerts  |  /api/stats  |  /api/ips                   │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP polling (2–5s)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              React Dashboard  (port 5173)                    │
│   StatCards | TrafficChart | PieChart | AlertTable | TopIPs  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

| Technology                                                                                                                               | Version | Purpose                             |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ------- | ----------------------------------- |
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square) **Python**                          | 3.10+   | Core language                       |
| ![FastAPI](https://img.shields.io/badge/-FastAPI-009688?logo=fastapi&logoColor=white&style=flat-square) **FastAPI**                      | 0.135   | REST API framework                  |
| ![Uvicorn](https://img.shields.io/badge/-Uvicorn-4B5563?logo=gunicorn&logoColor=white&style=flat-square) **Uvicorn**                     | 0.42    | ASGI server                         |
| ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?logo=postgresql&logoColor=white&style=flat-square) **PostgreSQL**          | 16      | Primary database                    |
| ![psycopg2](https://img.shields.io/badge/-psycopg2-336791?logo=postgresql&logoColor=white&style=flat-square) **psycopg2**                | 2.9     | PostgreSQL driver + connection pool |
| ![Scapy](https://img.shields.io/badge/-Scapy-1F6F8B?logo=python&logoColor=white&style=flat-square) **Scapy**                             | 2.7     | Packet capture & crafting           |
| ![scikit-learn](https://img.shields.io/badge/-scikit--learn-F7931E?logo=scikit-learn&logoColor=white&style=flat-square) **scikit-learn** | 1.8     | Random Forest classifier            |
| ![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white&style=flat-square) **Pandas**                          | 3.0     | Data processing for ML              |
| ![NumPy](https://img.shields.io/badge/-NumPy-013243?logo=numpy&logoColor=white&style=flat-square) **NumPy**                              | 2.4     | Numerical operations                |
| ![Pydantic](https://img.shields.io/badge/-Pydantic-E92063?logo=pydantic&logoColor=white&style=flat-square) **Pydantic**                  | 2.12    | Request/response validation         |
| **python-dotenv**                                                                                                                        | 1.2     | Environment variable management     |

### Frontend

| Technology                                                                                                           | Version | Purpose                 |
| -------------------------------------------------------------------------------------------------------------------- | ------- | ----------------------- |
| ![React](https://img.shields.io/badge/-React-61DAFB?logo=react&logoColor=black&style=flat-square) **React**          | 18.3    | UI framework            |
| ![Vite](https://img.shields.io/badge/-Vite-646CFF?logo=vite&logoColor=white&style=flat-square) **Vite**              | 5.4     | Build tool & dev server |
| ![Axios](https://img.shields.io/badge/-Axios-5A29E4?logo=axios&logoColor=white&style=flat-square) **Axios**          | 1.13    | HTTP client             |
| ![Recharts](https://img.shields.io/badge/-Recharts-22B5BF?logo=react&logoColor=white&style=flat-square) **Recharts** | 3.8     | Line chart & pie chart  |

### ML / Dataset

|                     | Details                                                                                              |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| **Dataset**         | [UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset) — ~175,000 network flow records |
| **Model**           | Random Forest (100 estimators, max_depth=20, balanced class weights)                                 |
| **Features used**   | `proto`, `service`, `state`, `dur`, `sbytes`, `dbytes`, `sttl`, `dttl`, `sloss`, `dloss`             |
| **Alert threshold** | Attack probability > 75%                                                                             |

---

## 📁 Project Structure

```
hybrid-ids/
│
├── backend/
│   ├── main.py                    # FastAPI app + sniffer startup
│   ├── requirements.txt
│   ├── .env                       # DB credentials (create this)
│   │
│   ├── api/
│   │   ├── routes_alerts.py       # GET /alerts, POST /alerts/manual
│   │   ├── routes_stats.py        # GET /stats/summary, /stats/traffic
│   │   └── routes_ips.py          # GET /ips/top, /ips/blocked, POST /ips/block
│   │
│   ├── capture/
│   │   ├── sniffer.py             # Scapy sniff loop + traffic rate thread
│   │   └── feature_extractor.py  # Packet → feature dict + ML vector
│   │
│   ├── detection/
│   │   ├── rule_engine.py         # Port scan / brute force / DoS rules
│   │   └── ml_engine.py           # Random Forest inference
│   │
│   ├── db/
│   │   ├── connection.py          # psycopg2 thread-safe connection pool
│   │   ├── queries.py             # All SQL queries
│   │   └── schema.sql             # Table definitions + indexes
│   │
│   └── models/
│       ├── train.py               # One-time training script
│       ├── UNSW_NB15_training-set.csv   # (download separately)
│       ├── UNSW_NB15_testing-set.csv    # (download separately)
│       ├── model.pkl              # Generated after training
│       └── model_meta.pkl         # Encoders + feature list
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js             # Proxy /api → localhost:8000
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── api/client.js          # Axios instance
│       ├── hooks/
│       │   ├── useAlerts.js       # Polls /api/alerts every 2s
│       │   ├── useStats.js        # Polls /api/stats every 3s
│       │   └── useTraffic.js      # Polls /api/stats/traffic every 3s
│       ├── components/
│       │   ├── NavBar.jsx
│       │   ├── StatCard.jsx
│       │   ├── TrafficChart.jsx
│       │   ├── AttackPieChart.jsx
│       │   ├── AlertTable.jsx
│       │   └── TopIPsTable.jsx
│       └── pages/
│           └── Dashboard.jsx
│
└── scripts/
    ├── simulate_portscan.py       # Sends TCP SYNs to 59 ports
    ├── simulate_bruteforce.py     # Sends 30 SYNs to port 22
    └── simulate_dos.py            # Floods 200 SYNs to port 80
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** — [python.org](https://python.org)
- **Node.js 18+** — [nodejs.org](https://nodejs.org)
- **PostgreSQL 14+** — [postgresql.org](https://postgresql.org)
- **Npcap** (Windows) or **libpcap** (Linux/macOS) — required by Scapy
  - Windows: [npcap.com](https://npcap.com)
  - Linux: `sudo apt install libpcap-dev`
  - macOS: `brew install libpcap`
- **Admin / root privileges** — required for raw packet sniffing

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ayush-2404/Sentinel_IDS.git
cd Sentinel_IDS
```

### 2. Set Up the Database

Connect to PostgreSQL and create a database:

```sql
CREATE DATABASE ids_db;
```

Then run the schema file to create all tables and indexes:

```bash
psql -U postgres -d ids_db -f backend/db/schema.sql
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend/` directory:

```bash
# backend/.env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ids_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 4. Set Up the Python Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### 5. Set Up the React Frontend

```bash
cd frontend
npm install
```

---

## 🤖 Training the ML Model

The ML engine requires a trained model before the backend will perform anomaly detection.

### Step 1 — Download the UNSW-NB15 Dataset

Download the CSV files from the [official UNSW-NB15 page](https://research.unsw.edu.au/projects/unsw-nb15-dataset) and place them in `backend/models/`:

```
backend/models/UNSW_NB15_training-set.csv
backend/models/UNSW_NB15_testing-set.csv
```

### Step 2 — Run the Training Script

```bash
# From the backend/ directory with venv activated
cd backend
python -m models.train
```

This will:

- Load and preprocess ~175k rows using 10 selected features
- Encode categorical columns (`proto`, `service`, `state`) with LabelEncoder
- Train a Random Forest with 100 estimators across all CPU cores
- Print accuracy and a full classification report
- Save `model.pkl` and `model_meta.pkl` to `backend/models/`

> Training takes approximately **1–2 minutes** depending on your hardware.

**Expected output:**

```
[Train] Training set: 175341 samples
[Train] Test set:     82332 samples
[Train] Attack ratio in training: 46.5%
[Train] Training Random Forest (this takes ~1-2 mins)...

[Train] === Results ===
Accuracy: 0.9XXX
              precision    recall  f1-score
      Normal     0.XX       0.XX     0.XX
      Attack     0.XX       0.XX     0.XX

[Train] Saved model  → backend/models/model.pkl
[Train] Saved meta   → backend/models/model_meta.pkl
```

---

## ▶️ Running the Application

You need **three terminals** open simultaneously.

### Terminal 1 — Start the Backend (requires admin/root)

```bash
cd backend
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Linux / macOS — root required for raw sockets
sudo venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Windows — run terminal as Administrator
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:

```
[ML Engine] Model + encoders loaded (UNSW-NB15).
[Main] Sniffer thread started.
[Sniffer] Starting packet capture...
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 — Start the Frontend

```bash
cd frontend
npm run dev
```

You should see:

```
  VITE v5.x.x  ready in XXX ms
  ➜  Local:   http://localhost:5173/
```

### Terminal 3 — (Optional) Run Simulations

See the [Attack Simulations](#-attack-simulations) section below.

### Access the Dashboard

Open your browser and navigate to:

```
http://localhost:5173
```

The API docs (Swagger UI) are available at:

```
http://localhost:8000/docs
```

---

## 🧪 Attack Simulations

Three simulation scripts are included to generate test traffic and verify detections. They both send real Scapy packets **and** call the manual alert API endpoint to guarantee the dashboard shows the correct attack type.

> ⚠️ **Update the `TARGET` IP** in each script to match your machine's actual local IP address (find it with `ipconfig` on Windows or `ip addr` on Linux).

### Run from the `scripts/` directory (with venv activated, as admin):

```bash
# Simulate a Port Scan — probes 59 ports
python scripts/simulate_portscan.py

# Simulate a Brute Force — 30 SYNs to port 22 (SSH)
python scripts/simulate_bruteforce.py

# Simulate a DoS Flood — 200 SYNs to port 80 in ~2 seconds
python scripts/simulate_dos.py
```

Each script will print a confirmation and the alert will appear in the Live Alert Feed on the dashboard within 2 seconds.

| Script                   | Fake Source IP | Attack Type   | Packets Sent                  |
| ------------------------ | -------------- | ------------- | ----------------------------- |
| `simulate_portscan.py`   | `10.0.0.99`    | `port_scan`   | 59 TCP SYNs across ports 1–59 |
| `simulate_bruteforce.py` | `10.0.0.101`   | `brute_force` | 30 TCP SYNs to port 22        |
| `simulate_dos.py`        | `10.0.0.100`   | `dos_attack`  | 200 TCP SYNs to port 80       |

---

## 📡 API Reference

Base URL: `http://localhost:8000`

### Alerts

| Method | Endpoint             | Description                                   |
| ------ | -------------------- | --------------------------------------------- |
| `GET`  | `/api/alerts/`       | Get recent alerts (default: last 50)          |
| `GET`  | `/api/alerts/types`  | Get alert counts grouped by attack type       |
| `GET`  | `/api/alerts/count`  | Get total alert count                         |
| `POST` | `/api/alerts/manual` | Manually create an alert (used by simulators) |

**POST `/api/alerts/manual` body:**

```json
{
  "src_ip": "10.0.0.99",
  "attack_type": "port_scan",
  "confidence": 1.0,
  "details": "Scanned 59 ports in 1.2s"
}
```

### Stats

| Method | Endpoint             | Description                                    |
| ------ | -------------------- | ---------------------------------------------- |
| `GET`  | `/api/stats/summary` | Total packets, alerts, and blocked IPs         |
| `GET`  | `/api/stats/traffic` | Recent packets/sec readings (default: last 30) |

### IPs

| Method | Endpoint           | Description                                      |
| ------ | ------------------ | ------------------------------------------------ |
| `GET`  | `/api/ips/top`     | Top source IPs by packet count (default: top 10) |
| `GET`  | `/api/ips/blocked` | List all blocked IPs                             |
| `POST` | `/api/ips/block`   | Manually block an IP                             |

---

## 🗄️ Database Schema

```sql
-- All captured network packets
packets (id, src_ip, dst_ip, src_port, dst_port, protocol, length, timestamp)

-- Alerts from rule engine and ML engine
alerts (id, src_ip, attack_type, confidence, details, timestamp)

-- IPs blocked automatically or manually
blocked_ips (id, ip_address UNIQUE, reason, blocked_at)

-- Traffic rate samples recorded every 5 seconds
traffic_stats (id, packets_per_sec, recorded_at)
```

Indexes are created on `alerts(timestamp DESC)`, `packets(src_ip)`, and `traffic_stats(recorded_at DESC)` for fast dashboard queries.

---

## 🔬 How Detection Works

### Rule Engine (`detection/rule_engine.py`)

Uses a **15-second sliding window** per source IP. Checks three conditions on every incoming packet:

| Attack          | Trigger                                               | Threshold    |
| --------------- | ----------------------------------------------------- | ------------ |
| **Port Scan**   | Distinct destination ports from one IP in 15s         | > 5 ports    |
| **Brute Force** | Repeated requests from one IP to the same port in 15s | > 8 requests |
| **DoS Attack**  | Total packets from one IP in 5s                       | > 30 packets |

Alerts are **deduplicated** — the same attack type from the same IP won't fire again for 30 seconds. Whitelisted IPs (localhost, your machine's IP) are skipped entirely.

### ML Engine (`detection/ml_engine.py`)

Each packet is mapped to a 10-feature vector approximating the UNSW-NB15 flow schema. The Random Forest model outputs a probability. If `P(attack) > 0.75`, a `ml_anomaly` alert is inserted and the IP is blocked.

Feature approximations for single packets:

- `sbytes` ← packet length
- `sttl` ← IP TTL field
- `dur`, `dbytes`, `dttl`, `sloss`, `dloss` ← set to 0 (unknown for single packets)
- `state` ← hardcoded to `"INT"` (in-progress)

---

## ⚙️ Configuration

### Rule Engine Thresholds (`backend/detection/rule_engine.py`)

```python
PORT_SCAN_THRESHOLD   = 5    # distinct ports in WINDOW_SECONDS
BRUTE_FORCE_THRESHOLD = 8    # requests to same port in WINDOW_SECONDS
DOS_THRESHOLD         = 30   # total packets in 5s
WINDOW_SECONDS        = 15
```

### ML Confidence Threshold (`backend/detection/ml_engine.py`)

```python
if attack_prob > 0.75:   # change this to tune sensitivity
```

### IP Whitelist (`backend/detection/rule_engine.py`)

```python
self.WHITELIST = {
    "127.0.0.1",
    "::1",
    "192.168.1.7",   # replace with your machine's actual IP
}
```

### Sniffer Interface (`backend/main.py`)

```python
# None = sniff on all interfaces
# Set to e.g. "eth0" or "Wi-Fi" to target a specific interface
start_sniffing(interface=None)
```

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Built for educational and research purposes · Hybrid IDS
</div>
