# 🚀 WAFilter Pro: WhatsApp Availability Checker

**WAFilter Pro** is a high-performance, professional-grade Python application designed to filter and verify WhatsApp-registered phone numbers from any Excel or CSV list. It uses browser automation via Selenium to check numbers without the need for expensive official APIs.

---

## ✨ Key Features

- 🎨 **Modern UI/UX**: Built with **PyQt6**, featuring a sleek dashboard, custom animations, and a responsive sidebar.
- 📊 **Real-time Analytics**: Live statistics cards for total numbers, valid accounts, and invalid entries.
- 📁 **Universal Upload**: Support for `.xlsx`, `.xls`, and `.csv` files with automatic column detection.
- 🤖 **Smart Automation**: Uses Selenium + ChromeDriver to navigate WhatsApp Web intelligently.
- 📥 **Filtered Export**: One-click download for valid WhatsApp numbers or a full checking report.
- 🛡️ **Safety Algorithms**: Integrated random delays and human-like interaction patterns to protect your WhatsApp account from flags.
- 🧵 **Multi-threaded**: The UI remains fluid and responsive even during large batch processing.

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **GUI Framework**: PyQt6
- **Automation**: Selenium WebDriver
- **Data Processing**: Pandas, OpenPyXL
- **Driver Management**: webdriver-manager (Automatic ChromeDriver setup)

---

## 🏁 Prerequisites

Before running the application, ensure you have:
1.  **Python 3.8+** installed.
2.  **Google Chrome** installed on your system.

---

## ⚙️ Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/PromitaMajhi/WAFilter-Pro.git
    cd WAFilter-Pro
    ```

2.  **Install Dependencies**:
    Execute the following command in your terminal/command prompt:
    ```bash
    pip install PyQt6 selenium pandas openpyxl webdriver-manager
    ```

---

## 🚀 How to Run the Software

To launch the application, run the `main.py` entry point:

```bash
python whatsapp_checker/main.py
```

### 📖 Step-by-Step Usage Guide

1.  **Launch WAFilter Pro**: Once the GUI opens, you'll see the main Dashboard.
2.  **Upload Your List**: Click the **"Upload Excel/CSV"** button. The software will automatically detect your phone numbers and update the "Total Detected" card.
3.  **Start the Process**: Click **"Start Checking"**. 
4.  **WhatsApp Login**: A Chrome browser window will appear. **Scan the QR code** using your phone (WhatsApp > Linked Devices).
5.  **Sit Back & Relax**: The software will now automatically check each number. You can monitor progress through the progress bar, live table, and automation logs.
6.  **Export Results**: Once the status says "Completed", use the **"Download Valid Only"** button to save your filtered WhatsApp list.

---

## 📂 Project Structure

```text
whatsapp_checker/
│
├── main.py                # Application entry point
├── ui/
│   └── dashboard.py       # PyQt6 GUI layout and logic
├── automation/
│   └── checker.py        # Selenium-based WhatsApp checking logic
├── utils/
│   └── excel_handler.py   # File reading/writing utilities
├── assets/                # Icons and branding assets
└── output/                # Default results directory
```

---

## ⚠️ Safety Precautions

- **Avoid Overuse**: We recommend checking no more than 500-1000 numbers per day on a single account to stay within WhatsApp's safety thresholds.
- **Warm-up Your Account**: Use an established WhatsApp account rather than a brand-new one for better reliability.
- **Delays**: Do not set delays too low. The default random delay is designed to mimic natural human behavior.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Created with ❤️ by the WAFilter Pro Team*
