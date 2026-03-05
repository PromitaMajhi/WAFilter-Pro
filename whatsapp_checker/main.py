import sys
import os

# Add the root directory to sys.path so that we can import from ui, automation, etc.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.dashboard import Dashboard

def main():
    app = QApplication(sys.argv)
    
    # Optional: Force style for consistent modern look across platforms
    app.setStyle("Fusion")
    
    window = Dashboard()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
