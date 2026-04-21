# 🏥 SHA Claim Automator

> An intelligent browser automation tool that reduced SHA (Social Health Authority) medical claim processing time from **20 minutes to 5 seconds** — a **240x speed improvement** — eliminating the need for 3 full-time staff working 12+ hour shifts.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Async-green?logo=microsoft&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-40%20Passed-brightgreen?logo=pytest&logoColor=white)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black?logo=github-actions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 💥 Real-World Impact

| Metric | Before | After |
|---|---|---|
| ⏱️ Time per claim | 20 minutes | **5 seconds** |
| 👥 Staff required | 3 people | **1 automated script** |
| 🕐 Working hours | 12+ hours/day | **Runs instantly** |
| 🚀 Speed improvement | — | **240x faster** |
| 🏗️ Time to build | — | **4 months** |

> This tool replaced a full manual workflow performed by a team of 3 people working over 12 hours a day.

---

## 📌 Overview

The **SHA Claim Automator** is a production-ready automation tool designed to eliminate manual data entry in SHA medical billing workflows in Kenya. It automatically:

- 🔍 **Detects patient type** (Child / Adult) from the portal UI
- 🩺 **Selects a clinically appropriate diagnosis** from a curated ICD-10 pool
- 💊 **Fills in billing categories** — Prescription, Lab, and Consultation
- 💾 **Submits the claim** with retry logic and robust error handling

Built for real-world reliability with full async support, modular architecture, and a comprehensive test suite.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🤖 **Smart Patient Detection** | Automatically identifies child vs adult patients from live UI state |
| 🩺 **ICD-10 Diagnosis Pool** | Curated list of valid diagnoses mapped to correct SHA billing tariffs |
| 💰 **Automated Billing** | Fills prescription, lab, and consultation amounts per SHA rates |
| 🔁 **Retry Logic** | All critical actions retry up to 5 times with configurable delays |
| ⚡ **Async Architecture** | Built on Python `asyncio` + Playwright for fast, non-blocking execution |
| 🧪 **Test Suite** | 40 unit tests with mocked Playwright pages using `pytest-asyncio` |
| 🔄 **CI/CD Pipeline** | GitHub Actions workflow runs tests on every push and pull request |

---

## 🏗️ Project Structure

```
sha-claim-automator/
├── src/
│   ├── __init__.py          # Package initializer
│   ├── automator.py         # Main orchestrator class (SHAClaimAutomator)
│   ├── billing.py           # Billing panel automation (open, select, fill, save)
│   ├── diagnosis.py         # Patient detection & diagnosis selection
│   └── utils.py             # Shared helpers (wait, click, type, find elements)
├── tests/
│   ├── conftest.py          # Shared pytest fixtures (mock page, prices, diagnoses)
│   ├── test_billing.py      # Unit tests for billing module
│   ├── test_diagnosis.py    # Unit tests for diagnosis module
│   └── test_utils.py        # Unit tests for utils module
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Google Chrome / Chromium

### 1. Clone the repository
```bash
git clone https://github.com/Gerald-makernext/sha-claim-automator.git
cd sha-claim-automator
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browser
```bash
playwright install chromium
```

### 5. Configure environment
```bash
cp .env.example .env
# Edit .env and set your SHA portal URL
```

---

## 🧪 Running Tests

```bash
pytest
```

Expected output:
```
collected 40 items
........................................
40 passed in 10.77s
```

---

## 🔄 CI/CD Pipeline

Every push to `main` triggers the GitHub Actions pipeline which:

1. ✅ Sets up Python 3.11
2. ✅ Installs all dependencies
3. ✅ Installs Playwright Chromium browser
4. ✅ Runs the full test suite

---

## 🧠 How It Works

```
Browser Launch
      │
      ▼
Navigate to SHA Portal
      │
      ▼
Detect Patient Type (Child / Adult)
      │
      ▼
Select Random ICD-10 Diagnosis
      │
      ▼
Select Diagnosis on Page
      │
      ▼
Open Billing Panel
      │
      ├──▶ Prescription → Enter Amount → Save
      ├──▶ Lab          → Enter Amount → Save
      └──▶ Consultation → Enter Amount → Save
                │
                ▼
         Claim Submitted ✅ (in ~5 seconds)
```

---

## 🛠️ Tech Stack

- **[Python 3.12](https://www.python.org/)** — Core language
- **[Playwright](https://playwright.dev/python/)** — Browser automation
- **[pytest](https://pytest.org/)** + **[pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** — Testing framework
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — Environment configuration
- **[GitHub Actions](https://github.com/features/actions)** — CI/CD pipeline

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and adapt it.

---

## 👤 Author

**Gerald**
- GitHub: [@Gerald-makernext](https://github.com/Gerald-makernext)

---

> 💡 *Built to solve a real healthcare administration crisis in Kenya — transforming a 12-hour manual billing process into a fully automated 5-second workflow per claim*