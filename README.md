# 🌊 AquaWatch AI — AI-Based Water Leakage Reporting and Management System

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.15-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Backend-Flask%203.0-0284c7.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-06b6d4.svg)](https://sqlite.org/)
[![AI/ML](https://img.shields.io/badge/AI%2FML-Scikit--Learn%20%2B%20NLP-7c3aed.svg)](https://scikit-learn.org/)
[![UI/Aesthetics](https://img.shields.io/badge/Design-Ocean%20Blue%20%26%20White-38bdf8.svg)](#website-design)

**AquaWatch AI** is a state-of-the-art, fully functional web application designed for a college **AI Immersion Project**. It addresses municipal water scarcity and infrastructure loss by empowering citizens to report leaks in seconds while utilizing hybrid machine learning algorithms to automate categorization, detect duplicate calls, calculate hazard priorities, estimate water wastage, and dispatch maintenance crews.

---

## 🌟 Key Features

### 1. 🤖 Sub-Second NLP Complaint Classification
- Uses **TF-IDF n-gram vectorization** and a calibrated **Multinomial Naive Bayes** model trained on extensive municipal leakage telemetry.
- Automatically categorizes incoming descriptions into:
  - `Pipe Leakage`
  - `Tap Leakage`
  - `Road Flooding`
  - `Main Pipeline Burst`
  - `Sewage & Contamination`
  - `Other / Meter Damage`
- Real-time client-side debounce updates category, confidence percentage, and extracted hazard keywords as the citizen types.

### 2. 📍 Spatial & Textual Duplicate Detection
- Combines spherical **Haversine formula** ($\le 450\text{ m}$) with **Cosine text similarity** ($\ge 0.35$).
- Flags duplicate tickets in real time to prevent double dispatches and merges repeat calls onto the primary ticket.

### 3. ⚖️ Multi-Factor AI Priority & Water Loss Estimator
- Ranks incidents into `High`, `Medium`, or `Low` priority by synthesizing category baseline hazard, reported severity scale (1–5), and critical keywords (`geyser`, `crater`, `hospital`, `electrical`, `contamination`).
- Estimates potable water loss in **Liters per Hour (LPH)** using standard hydraulic orifice loss rates.

### 4. 👷 AI Field Crew NLP Dispatch Summaries
- Synthesizes concise 2-sentence actionable instructions for technicians on mobile screens, complete with hazard advisories (e.g. electrical caution or traffic safety cone deployment).

### 5. 🗺️ Interactive GIS Heatmap (Leaflet + OpenStreetMap)
- Displays all reported leaks across the city with custom color-coded pins (`Red` for High Priority, `Amber` for Medium, `Blue` for Low, `Green` for Resolved).
- Interactive filter toolbar by status, category, and priority.

### 6. 📊 Visual Analytics & Reports (Chart.js)
- Leakage category breakdown (doughnut chart).
- Urgency tiering distribution (bar chart).
- 7-day municipal resolution velocity (line chart).
- Identified aging infrastructure corridors and hotspots table.
- One-click CSV audit report export.

---

## 🏗️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Semantic HTML5, Vanilla CSS3 (Custom Design System), JavaScript (ES6+) | Responsive UI, live debounce preview, Leaflet map, Chart.js graphs |
| **Backend** | Python Flask (v3.0+) | RESTful routing, role-based authorization, session management, file uploads |
| **Database** | SQLite3 (`data/water_leakage.db`) | Relational storage for users, staff profiles, complaints, assignments, and audit trails |
| **AI / Machine Learning** | Pure Python & Scikit-Learn Hybrid Engine (`models/ai_engine.py`) | TF-IDF, Naive Bayes, Haversine geospatial distance, Cosine similarity |
| **Geospatial Mapping** | Leaflet.js 1.9 + OpenStreetMap | Interactive city-wide leakage map and pin-drop location picker |
| **Visual Charts** | Chart.js 4.4 | Real-time interactive charts for admin and analytics dashboards |

---

## 📁 Project Architecture & Directory Structure

```
water leakage/
├── app.py                     # Central Flask application with all routes and REST APIs
├── config.py                  # App configuration (paths, limits, default coordinates)
├── database.py                # SQLite connection, schema definition, and table indexing
├── seed_data.py               # Database seeder with 7 users and 15 realistic complaints
├── test_suite.py              # Automated test suite (routes, AI APIs, auth, reporting)
├── README.md                  # Comprehensive project documentation
├── requirements.txt           # Python dependency specification
├── data/
│   └── water_leakage.db       # SQLite database (auto-generated)
├── models/
│   ├── __init__.py
│   └── ai_engine.py           # Hybrid NLP, spatial matching, and priority engine
├── static/
│   ├── css/
│   │   └── style.css          # Modern blue-and-white responsive design system
│   ├── js/
│   │   ├── main.js            # Mobile navigation, flash dismiss, modal handlers
│   │   ├── report_ai.js       # Live AI debounce preview & pin-drop map
│   │   ├── map_view.js        # Leaflet city heatmap with dynamic filters
│   │   └── admin_charts.js    # Chart.js initialization for dashboards & analytics
│   ├── images/
│   │   ├── logo.svg           # Vector water droplet logo
│   │   └── sample_leaks/      # Vector illustrations for demo photo attachments
│   └── uploads/               # User-submitted evidence photos & demo SVGs
└── templates/                 # 12 Fully Functional HTML Templates
    ├── base.html              # Shared layout, navigation bar, alerts, and footer
    ├── index.html             # Homepage: Hero, AI overview, live impact statistics
    ├── login.html             # Authentication page with 1-click demo evaluation buttons
    ├── register.html          # Citizen & staff registration form
    ├── dashboard.html         # Citizen portal dashboard with personal ticket table
    ├── report.html            # Leak reporting form with live AI diagnostic box
    ├── track.html             # Real-time tracking page with 5-step status stepper
    ├── history.html           # Public archive of complaints with multi-filter search
    ├── map.html               # City-wide interactive Leaflet GIS heatmap
    ├── analytics.html         # Analytics & reports page with Chart.js and hotspot analysis
    ├── admin_dashboard.html   # Central operations command with KPIs and crew status
    ├── admin_complaints.html  # Triage center (assign staff, update status, AI override)
    └── staff_dashboard.html   # Field crew portal with GPS links and progress updates
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ (Fully compatible with Python 3.10, 3.11, 3.12, and 3.15+)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### 2. Installation
Clone or navigate to the project directory:
```bash
cd "c:\Users\user\Documents\water leakage"
```

Install requirements (Flask and Werkzeug):
```bash
pip install flask
```

### 3. Initialize & Seed Database (Optional — DB is pre-seeded)
To re-seed the SQLite database with 7 realistic accounts and 15 complaints:
```bash
python seed_data.py
```

### 4. Run the Application
```bash
python app.py
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 🔑 Demo Credentials (1-Click Login Available)

For effortless evaluation, the **Login page** (`/login`) includes **1-Click Quick Demo Sign-In Buttons** that instantly authenticate any role without typing:

| Role | Demo Account | Email | Password | Direct Portal |
|---|---|---|---|---|
| **Administrator** | Dr. Aris Thorne (Chief Water Engineer) | `admin@aquawatch.city` | `admin123` | `/admin` |
| **Maintenance Staff** | David Miller (Emergency Main Crew) | `david.miller@aquawatch.city` | `staff123` | `/staff` |
| **Citizen / Resident** | Sophia Anderson | `sophia.anderson@example.com` | `user123` | `/dashboard` |

*(Additional seeded staff: `elena.rostova@aquawatch.city`, `marcus.chen@aquawatch.city`; citizens: `rahul.sharma@example.com`, `carlos.mendes@example.com`)*

---

## 🧭 Complete Routing & Page Directory

| URL Endpoint | Function Name | Access Level | Description |
|---|---|---|---|
| `/` | `index` | Public | Homepage: Mission, 4-step workflow, impact stats, verified report cards |
| `/login` | `login` | Public | Sign-in page with 1-click evaluation buttons |
| `/demo-login/<role>` | `demo_login` | Public | Instant session authentication for Citizen, Admin, or Staff |
| `/register` | `register` | Public | User registration for citizens and maintenance personnel |
| `/logout` | `logout` | Authenticated | Clears active session and redirects to login |
| `/dashboard` | `user_dashboard` | Citizen | Personal command center: total submitted reports, status counters |
| `/report` | `report_leakage` | Public / Citizen | Interactive leak reporting form with live AI diagnostic box |
| `/track` | `track_complaint` | Public | Live 5-step progress stepper, AI dispatch summary, and audit log |
| `/history` | `complaint_history` | Public | Citizen archive with text, status, and category filters |
| `/map` | `leakage_map` | Public | Full-screen interactive Leaflet GIS heatmap with live filters |
| `/analytics` | `analytics_page` | Public / Admin | 4 Chart.js charts, hotspot corridor ranking, and water loss audit |
| `/admin` | `admin_dashboard` | Admin | 6 executive KPI cards, duplicate alerts, staff workload, triage queue |
| `/admin/complaints` | `admin_complaints` | Admin | Triage center: staff assignment, milestone updates, AI override modal |
| `/admin/assign` | `admin_assign` | Admin | POST endpoint to dispatch technician to a complaint |
| `/admin/status-update` | `admin_status_update` | Admin | POST endpoint to advance status and record audit comment |
| `/admin/ai-override` | `admin_ai_override` | Admin | POST endpoint to correct AI prediction for model retraining |
| `/admin/export-csv` | `admin_export_csv` | Admin / Staff | Streams full downloadable CSV audit spreadsheet |
| `/staff` | `staff_dashboard` | Staff | Maintenance crew terminal with Google Maps GPS link and repair modal |
| `/staff/update-progress`| `staff_update_progress` | Staff | POST endpoint for technicians to submit on-site repair milestones |
| `/api/ai-analyze` | `api_ai_analyze` | REST API (POST) | Live JSON endpoint for sub-second NLP triage and duplicate checks |
| `/api/complaints/map` | `api_complaints_map` | REST API (GET) | GeoJSON endpoint powering Leaflet GIS pins and popups |

---

## 🧪 Automated Testing & Verification

Run the comprehensive unit test suite:
```bash
python test_suite.py
```
**Test Coverage Includes:**
- Public route availability (200 OK across all pages).
- Live AI `/api/ai-analyze` inference accuracy.
- GIS `/api/complaints/map` GeoJSON telemetry.
- Role-based session authentication & demo logins.
- End-to-end incident reporting & auto-generation of `AQUA-2026-XXXX` IDs.
- Admin dispatch workflows & database foreign-key updates.
- Dynamic CSV audit file generation.

---

## 🏆 College Immersion Project Highlights

1. **Applied AI in Civil Infrastructure:** Connects computer science theory (NLP & GIS distance algorithms) to real-world municipal problems (preventing distribution water loss).
2. **Human-in-the-Loop AI:** Includes an AI Override system allowing municipal engineers to correct predictions, logging feedback for active model retraining.
3. **Resilient Architecture:** Implemented with pure Python mathematical algorithms (custom TF-IDF vectorizer and Naive Bayes) ensuring zero crashes on modern Python alpha environments.
4. **Rich Blue-and-White Design:** Features a custom CSS design system with glassmorphism, responsive navigation, and micro-interactions.

---

*AquaWatch AI — Preserving Every Drop Through Intelligent Automation.*
