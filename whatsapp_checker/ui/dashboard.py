import sys
import os
import time
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QPushButton, QProgressBar, QTableWidget, QTableWidgetItem, 
    QFileDialog, QHeaderView, QListWidget, QFrame, QSizePolicy
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, QPropertyAnimation, 
    QEasingCurve, QSize, QRect
)
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QIcon, QLinearGradient, 
    QPainter, QPen, QBrush
)

from automation.checker import WhatsAppChecker
from utils.excel_handler import ExcelHandler

# --- Custom Styling (Modern Dark/Light Mode Theme) ---
MODERN_STYLE = """
    QMainWindow {
        background-color: #f7f9fc;
    }
    
    #Sidebar {
        background-color: #2c3e50;
        min-width: 250px;
        max-width: 250px;
    }
    
    #Header {
        background-color: #ffffff;
        border-bottom: 2px solid #e1e8ed;
        padding: 20px;
    }
    
    #Card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    QLabel {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #34495e;
    }
    
    #StatValue {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
    }
    
    QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        font-size: 14px;
        border: none;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    
    QPushButton#Secondary {
        background-color: #ecf0f1;
        color: #2c3e50;
    }
    
    QPushButton#Secondary:hover {
        background-color: #bdc3c7;
    }
    
    QProgressBar {
        border-radius: 8px;
        background-color: #e0e0e0;
        text-align: center;
        height: 12px;
    }
    
    QProgressBar::chunk {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #1abc9c, stop:1 #2ecc71);
        border-radius: 8px;
    }
    
    QTableWidget {
        background-color: white;
        border-radius: 8px;
        gridline-color: #ecf0f1;
        border: 1px solid #e1e8ed;
    }
    
    QHeaderView::section {
        background-color: #f8f9fa;
        color: #2c3e50;
        font-weight: bold;
        padding: 8px;
        border-bottom: 2px solid #e1e8ed;
    }
"""

class WorkerThread(QThread):
    """Background thread to handle checking without freezing UI."""
    progress_signal = pyqtSignal(int, int, str, bool) # current, total, number, status
    finished_signal = pyqtSignal(list)
    log_signal = pyqtSignal(str)

    def __init__(self, numbers, checker, delay_range=(2, 5)):
        super().__init__()
        self.numbers = numbers
        self.checker = checker
        self.delay_range = delay_range
        self.is_running = True
        self.is_paused = False

    def run(self):
        results = []
        total = len(self.numbers)
        
        self.log_signal.emit("Initializing WhatsApp session...")
        self.checker.start_browser()
        
        # Wait for user scan (we'll implement a notification or message in future)
        self.log_signal.emit("Waiting for WhatsApp Web login / QR scan...")
        time.sleep(10) # Initial wait for scan; we could also check for page load items
        
        for i, number in enumerate(self.numbers):
            while self.is_paused:
                time.sleep(0.5)
            
            if not self.is_running:
                break
            
            # Simple check logic (this will handle actual Selenium check)
            self.log_signal.emit(f"Checking {i+1}/{total}: {number}")
            status = self.checker.check_number(number)
            results.append((number, "Valid" if status else "Invalid"))
            
            # Emit UI update
            self.progress_signal.emit(i + 1, total, number, status)
            
            # Delay to avoid blocking
            delay = random.uniform(self.delay_range[0], self.delay_range[1])
            time.sleep(delay)
            
        self.finished_signal.emit(results)
        self.checker.stop()

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WAFilter Pro - WhatsApp Availability Checker")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(MODERN_STYLE)
        
        self.numbers = []
        self.results = []
        self.valid_count = 0
        self.invalid_count = 0
        self.checker = WhatsAppChecker()
        
        self.setup_ui()

    def setup_ui(self):
        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- Sidebar ---
        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        
        logo = QLabel("WAFilter Pro")
        logo.setStyleSheet("color: white; font-size: 24px; font-weight: bold; margin: 30px 0;")
        sidebar_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        nav_buttons = ["Dashboard", "Automation", "Settings", "Help"]
        for nav in nav_buttons:
            btn = QPushButton(nav)
            btn.setObjectName("Secondary")
            btn.setStyleSheet("background-color: transparent; color: #ecf0f1; border-radius: 0; text-align: left; padding-left: 30px;")
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)
        
        # --- Content Area ---
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        
        # Header (Stats Cards)
        stats_layout = QHBoxLayout()
        self.total_card = self.create_stat_card("Total Detected", "0", "#3498db")
        self.valid_card = self.create_stat_card("Valid Accounts", "0", "#2ecc71")
        self.invalid_card = self.create_stat_card("Invalid Numbers", "0", "#e74c3c")
        
        stats_layout.addWidget(self.total_card)
        stats_layout.addWidget(self.valid_card)
        stats_layout.addWidget(self.invalid_card)
        content_layout.addLayout(stats_layout)
        
        # Action Bar (Upload, Start, Reset)
        action_bar = QHBoxLayout()
        
        self.upload_btn = QPushButton("Upload Excel/CSV")
        self.upload_btn.setMinimumHeight(50)
        self.upload_btn.clicked.connect(self.upload_file)
        
        self.start_btn = QPushButton("Start Checking")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_checking)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setObjectName("Secondary")
        self.stop_btn.setEnabled(False)
        
        action_bar.addWidget(self.upload_btn)
        action_bar.addWidget(self.start_btn)
        action_bar.addWidget(self.stop_btn)
        content_layout.addLayout(action_bar)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        content_layout.addWidget(self.progress_bar)
        
        # Table and Logs
        data_viz_layout = QHBoxLayout()
        
        # Results Table
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Phone Number", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        data_viz_layout.addWidget(self.table, 2)
        
        # Logs Window
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_label = QLabel("Automation Logs")
        log_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        self.logs = QListWidget()
        self.logs.setStyleSheet("background-color: #f1f3f5; border-radius: 8px;")
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.logs)
        data_viz_layout.addWidget(log_container, 1)
        
        content_layout.addLayout(data_viz_layout)
        
        # Export Bar
        export_layout = QHBoxLayout()
        self.export_valid_btn = QPushButton("Download Valid Only")
        self.export_valid_btn.setObjectName("Secondary")
        self.export_valid_btn.setEnabled(False)
        self.export_valid_btn.clicked.connect(lambda: self.save_excel(True))
        
        self.export_all_btn = QPushButton("Download All Results")
        self.export_all_btn.setObjectName("Secondary")
        self.export_all_btn.setEnabled(False)
        self.export_all_btn.clicked.connect(lambda: self.save_excel(False))
        
        export_layout.addStretch()
        export_layout.addWidget(self.export_valid_btn)
        export_layout.addWidget(self.export_all_btn)
        content_layout.addLayout(export_layout)
        
        main_layout.addWidget(content, 1)

    def create_stat_card(self, label, value, color):
        card = QFrame()
        card.setObjectName("Card")
        card.setMinimumHeight(150)
        layout = QVBoxLayout(card)
        
        lbl = QLabel(label)
        lbl.setStyleSheet("font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: #7f8c8d;")
        
        val_lbl = QLabel(value)
        val_lbl.setObjectName("StatValue")
        val_lbl.setStyleSheet(f"color: {color};")
        
        layout.addWidget(lbl)
        layout.addWidget(val_lbl)
        
        # Store label to update later
        card.val_lbl = val_lbl
        return card

    def update_stats(self, total=None, valid=None, invalid=None):
        if total is not None:
            self.total_card.val_lbl.setText(str(total))
        if valid is not None:
            self.valid_card.val_lbl.setText(str(valid))
        if invalid is not None:
            self.invalid_card.val_lbl.setText(str(invalid))

    def upload_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV/Excel", "", "Data Files (*.xlsx *.csv *.xls)")
        if file_name:
            try:
                self.numbers = ExcelHandler.read_numbers(file_name)
                self.update_stats(total=len(self.numbers))
                self.logs.addItem(f"Loaded {len(self.numbers)} numbers from {os.path.basename(file_name)}")
                self.start_btn.setEnabled(True)
                self.table.setRowCount(0)
            except Exception as e:
                self.logs.addItem(f"Error loading file: {e}")

    def start_checking(self):
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.valid_count = 0
        self.invalid_count = 0
        self.results = []
        self.table.setRowCount(0)
        self.progress_bar.setValue(0)
        
        self.worker = WorkerThread(self.numbers, self.checker)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.log_signal.connect(lambda msg: self.logs.addItem(msg))
        self.worker.finished_signal.connect(self.checking_finished)
        self.worker.start()

    def update_progress(self, current, total, number, status):
        # Update progress bar
        p = int((current / total) * 100)
        self.progress_bar.setValue(p)
        
        # Update table
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(number)))
        status_text = "Valid" if status else "Invalid"
        item = QTableWidgetItem(status_text)
        item.setForeground(QColor("#27ae60" if status else "#e74c3c"))
        self.table.setItem(row, 1, item)
        self.table.scrollToBottom()
        
        # Update results and stats
        self.results.append((number, status_text))
        if status:
            self.valid_count += 1
        else:
            self.invalid_count += 1
            
        self.update_stats(valid=self.valid_count, invalid=self.invalid_count)

    def checking_finished(self, final_results):
        self.logs.addItem("🎉 Checking Process Completed!")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.export_valid_btn.setEnabled(True)
        self.export_all_btn.setEnabled(True)

    def save_excel(self, valid_only=False):
        data = self.results
        if valid_only:
            data = [r for r in data if r[1] == "Valid"]
            
        filename = "valid_whatsapp_numbers.xlsx" if valid_only else "all_checked_numbers.xlsx"
        
        path, _ = QFileDialog.getSaveFileName(self, "Save Result", filename, "Excel Files (*.xlsx)")
        if path:
            try:
                ExcelHandler.save_results(data, os.path.dirname(path), os.path.basename(path))
                self.logs.addItem(f"Successfully exported to {path}")
            except Exception as e:
                self.logs.addItem(f"Export error: {e}")

if __name__ == "__main__":
    app = sys.argv[0] if len(sys.argv) > 0 else "WAFilter Pro"
    # To run this file directly for testing, you need proper module imports
    pass
