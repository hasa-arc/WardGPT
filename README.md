# WardGPT
A special terminal-based work logger with timer, summaries, and payment estimates.

Here’s a detailed, ready‑to‑use `README.md` – you can drop it straight into your repository.


# WardGPT ⏱️

A colourful terminal‑based work logger that helps you track tasks, measure hours, and calculate payments – all with built‑in Python and zero extra dependencies.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [📸 Screenshot](#-screenshot)
- [🚀 Quick Start](#-quick-start)
- [📖 Detailed Usage](#-detailed-usage)
  - [Main Menu](#main-menu)
  - [1. Log a Task](#1-log-a-task)
  - [2. View / Manage Logs](#2-view--manage-logs)
  - [3. Summary](#3-summary)
  - [4. Payment Details](#4-payment-details)
  - [5. Exit](#5-exit)
- [💾 Data Storage](#-data-storage)
- [⚙️ Customization](#-customization)
- [📦 Building a Standalone App](#-building-a-standalone-app)
- [📜 License](#-license)

---

## ✨ Features

- **Three ways to log time**  
  ⏱ Live stopwatch (press Enter to start/stop)  
  🕒 Manual start & end times (24‑h format)  
  🔢 Direct hours entry  

- **Smart validation**  
  Prevents 0‑hour entries, warns on >16h days, rejects negative values.

- **Log management**  
  View all tasks in a clean numbered list, remove any task safely.

- **Rich summaries**  
  Total hours, average per task, longest & shortest tasks, days/weeks worked.

- **Payment estimates**  
  Configurable hourly rate, optional 20% tax deduction, net/gross calculation.

- **Beautiful interface**  
  ANSI colours, box‑drawing (╔═╗), auto‑clearing screens, dimmed prompts.

- **Local & private**  
  All data saved in your system’s standard application data folder – no cloud, no tracking.

- **Cross‑platform**  
  Works on macOS, Windows, and Linux. Data path adjusts automatically.

---

## 📸 Screenshot

> *(Add a screenshot of the main menu here – for example, `![Main Menu](screenshot.png)`)*

---

## 🚀 Quick Start

You only need Python 3.6 or newer. No external libraries are required.

```bash
git clone https://github.com/your-username/WardGPT.git
cd WardGPT
python3 wardgpt.py
```

If you prefer a shorter command:

```bash
python3 wardgpt.py
```
(in the folder containing `wardgpt.py`)

The program will automatically create its data file on first run.

---

## 📖 Detailed Usage

### Main Menu

```
╔══════════════════════════════════════╗
║            WardGPT v2.0             ║
╚══════════════════════════════════════╝
  📊 5 tasks | ⏱ 23.5h | 💰 £117.50

  1. Log a Task
  2. View / Manage Logs
  3. Summary
  4. Payment Details
  5. Exit
```

The status line shows total tasks, hours, and estimated earnings at a glance.

---

### 1. Log a Task

You’ll be asked for:
- **Date** – accepts many formats (DD/MM/YYYY, May 1 2026, 01‑05‑2026, …). Auto‑standardised.
- **Task Description** – minimum 3 characters.
- **Time tracking method**:
  - **Option 1 – Live Timer**: Press Enter to start, do your work, press Enter to stop. Elapsed time shown.
  - **Option 2 – Manual Times**: Enter start time and end time (e.g. 09:00 and 17:30). Handles overnight shifts.
  - **Option 3 – Direct Hours**: Just type the number of hours (e.g. 4.5).

All entries are validated:
- Hours must be > 0 and ≤ 24.
- A warning appears for entries > 16 hours (confirmation required).

---

### 2. View / Manage Logs

Sub‑menu:
- **View All Logs** – prints every logged task with date, description, and hours.
- **Remove a Task** – displays the list, then asks for the number to delete (0 to cancel). Saves immediately.

---

### 3. Summary

Displays:
- Total tasks and total hours
- Average hours per task
- Longest & shortest tasks (with their descriptions)
- Estimated payment
- Days worked (based on 8‑h day) and weeks worked (40‑h week)
- Last 3 logged tasks

---

### 4. Payment Details

Shows:
- Hourly rate
- Gross payment
- Tax estimate (20%) with net amount
- Time breakdown in days / weeks
- “Invoice‑ready” gross amount reminder

---

### 5. Exit

Saves data automatically, shows a goodbye banner, and waits for Enter (if you built the standalone app) so you can review before closing.

---

## 💾 Data Storage

All task logs are kept in a JSON file named `wardgpt.json`, located in:

| Platform | Path |
|----------|------|
| **macOS**   | `~/Library/Application Support/WardGPT/wardgpt.json` |
| **Windows** | `%APPDATA%\WardGPT\wardgpt.json` |
| **Linux**   | `~/.wardgpt/wardgpt.json` |

The JSON structure:
```json
{
  "log": [
    {
      "Date": "01 May 2026",
      "Task": "FCC Rental Monitoring",
      "Hours": 1.3
    }
  ]
}
```

You can manually edit or backup this file if needed.

---

## ⚙️ Customization

Open `wardgpt.py` and change these constants near the top:

```python
HOURLY_RATE = 5        # Your rate in £ (or $, €, …)
MAX_HOURS_PER_DAY = 24 # Maximum allowed hours per entry
```

The tax rate for the Payment screen is also adjustable – look for `tax_rate = 0.20` inside `show_payment()`.

After editing, the app works immediately – no rebuild required.

---

## 📦 Building a Standalone App

If you want a double‑clickable executable (no terminal command needed), use **PyInstaller**.

### 1. Install PyInstaller
```bash
pip3 install pyinstaller
```

### 2. Build the executable
```bash
cd /path/to/WardGPT
pyinstaller --onefile --name WardGPT wardgpt.py
```

The finished app will be in the `dist` folder:
- **macOS**: `dist/WardGPT` (move to `/Applications` if desired)
- **Windows**: `dist/WardGPT.exe`
- **Linux**: `dist/WardGPT`

You can even add a custom icon with `--icon=wardgpt.icns` (macOS) or `--icon=wardgpt.ico` (Windows).

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Pull requests are welcome! If you find a bug or have a feature idea, feel free to open an issue.

---

Built with ❤️ and core Python.
