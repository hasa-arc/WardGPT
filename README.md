# WardGPT
A special terminal-based work logger with timer, summaries, and payment estimates.
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


