import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class WhatsAppChecker:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--start-maximized")
        self.driver = None
        self.is_running = False
        self.is_paused = False

    def start_browser(self):
        """Initializes Chrome and waits for QR login."""
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.driver.get("https://web.whatsapp.com/")
        return self.driver

    def check_number(self, phone):
        """Checks if a phone number exists on WhatsApp."""
        if not self.driver:
            return None
        
        try:
            url = f"https://web.whatsapp.com/send?phone={phone}"
            self.driver.get(url)
            
            # Wait for main page to load or error message to appear
            wait = WebDriverWait(self.driver, 20)
            
            # Detect invalid number alert
            # The message is usually: "Phone number shared via URL is invalid"
            # It appears inside an alert box or modal.
            
            invalid_selectors = [
              "div[role='button'] div:contains('OK')", # Example selector for 'OK' button on alert
              "*[data-animate-modal-body='true']", # Typical modal body selector
              "div:contains('Phone number shared via url is invalid')", # Direct text check
              "div:contains('invalid')"
            ]
            
            # WhatsApp uses specific elements for message boxes vs invalid alerts
            # Wait for either:
            # 1. The message box (contenteditable='true') -> Valid
            # 2. An 'OK' button on an error modal or 'Phone number shared via url is invalid' -> Invalid
            
            # Using dynamic waits for better reliability
            try:
                # Wait for either condition
                WebDriverWait(self.driver, 20).until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']") or 
                             "invalid" in d.page_source.lower() or
                             d.find_elements(By.XPATH, "//*[contains(text(), 'OK')]")
                )
                
                # Check for invalid message first
                page_source = self.driver.page_source.lower()
                if "invalid" in page_source or "not shared via url" in page_source:
                    return False
                
                # If message box is present, it's valid
                if self.driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']"):
                    return True
                
                return False 
            except Exception:
                return False


        except Exception as e:
            print(f"Error checking {phone}: {e}")
            return False

    def stop(self):
        """Closes the browser session."""
        if self.driver:
            self.driver.quit()
        self.is_running = False

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False
