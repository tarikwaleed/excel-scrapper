from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import glob

class Scrapper:

    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None

    def _initialize_driver(self, download_dir=None):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        
        if download_dir:
            prefs = {
                "download.default_directory": download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            self.options.add_experimental_option("prefs", prefs)
        
        if self.headless:
            self.options.add_argument("--headless=new")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=self.options,
                                       service=Service(ChromeDriverManager().install()))

    def _set_download_directory(self, download_dir):
        if self.driver is not None:
            self.driver.quit()
        self._initialize_driver(download_dir)
    

    def download_file(self, resource, download_dir):
            # Ensure download directory exists
        os.makedirs(download_dir, exist_ok=True)
        
        # Delete existing files in the download directory
        for file_path in glob.glob(os.path.join(download_dir, '*'))+glob.glob(os.path.join(download_dir, '.*')):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted existing file: {file_path}")
                else:
                    print(f"Skipping non-file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        # Set the download directory for this specific file
        self._set_download_directory(download_dir)
        
        # Open the page and trigger the download
        self.driver.get(resource)
        
        # Login process
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        email_input = self.driver.find_element('id', 'Email')
        password_input = self.driver.find_element('id', 'Password')

        if email and password:
            email_input.send_keys(email)
            password_input.send_keys(password)
            login_button = self.driver.find_element('xpath', '//button[@type="submit"]')
            login_button.click()

        # Optional: Wait until the download completes, if necessary
        
        # Close the driver
        self.driver.quit()

