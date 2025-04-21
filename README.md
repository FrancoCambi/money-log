# 🗒️ MoneyLog

**MoneyLog** is a simple desktop application built with **Python** and **Tkinter** that helps you track your personal finances. You can log income and expenses, view your transaction history, and analyze your data through visual charts.

---

## Features

- 📥 Add income and expenses with category, amount, and sub-category.
- 📅 View transaction history by date.
- 📊 Visualize your financial data with bar and pie charts.
- 🗂️ Filter and sort by date, category, or type (income/expense).
- 💾 Data stored locally (json).

---

## 🛠️ Technologies used
- Python.
- Tkinter.
- Matplotlib.

---

## 🧪 Status: *Finished*
Finished. This project was just for fun and some learning. :)

---

## 🪟 How to Run MoneyLog on Windows

1. **Download the latest release**

   Go to the [Releases](https://github.com/FrancoCambi/money-log/releases) section of this repository and download the latest version's `.zip` file (e.g. `MoneyLog-v1.0.0.zip`).

2. **Run the application**

   Simply double-click the `.exe` file inside the compressed folder to launch MoneyLog. No installation is required.

---

If you see a warning from Windows SmartScreen, click **"More info"** and then **"Run anyway"**. This happens because the app is not signed with a certificate.

> 💡 The `.exe` version includes all required dependencies, including Tkinter and matplotlib.

---

## 🐧 How to Run MoneyLog on Linux

1. **Clone the repository**

   ```bash
   git clone https://github.com/your_username/moneylog.git
   cd moneylog
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   Make sure `pip` is up to date:

   ```bash
   pip install --upgrade pip
   ```

   Then install the required packages:

   ```bash
   pip install matplotlib
   ```

4. **Install Tkinter**

   Tkinter must be installed using your system's package manager. On Debian/Ubuntu-based systems:

   ```bash
   sudo apt update
   sudo apt install python3-tk
   ```

5. **Run the application**

   From the project root:

   ```bash
   python3 -m src/ui
   ```

   

