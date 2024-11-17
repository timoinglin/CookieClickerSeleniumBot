import os
import time
import glob
import logging
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import keyboard

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
SCRIPT_DIR = Path(__file__).resolve().parent
EXPORT_PATH = SCRIPT_DIR / "exports"

# Settings
CHECK_INTERVAL = 5          # Check every 5 seconds (Upgrades and products)
EXPORT_INTERVAL = 60        # Export every 60 seconds (Backups)
MAX_BACKUPS = 30            # Max backup files to keep
COOKIE_CLICK_DELAY = 0.01   # Delay between cookie clicks
WEBPAGE_LOAD_TIMEOUT = 15   # Max time to wait for page elements

def setup_driver():
    """
    Set up the Selenium WebDriver with the desired options.
    Returns:
        webdriver.Chrome: The configured Chrome WebDriver instance.
    """
    # Set up Chrome options
    chrome_options = Options()
    # Optionally set arguments
    # chrome_options.add_argument("--start-maximized")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Optionally set a custom window size (e.g., width=1200, height=800)
    driver.set_window_size(1450, 1030)  # Comment out if using start-maximized

    return driver

def accept_cookies_and_select_language(driver):
    """
    Accept the cookie policy and select the language on the Cookie Clicker website.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    """
    try:
        # Wait for and click the accept personal data button
        accept_button_xpath = '/html/body/div[3]/div[2]/div[2]/div[2]/div[2]/button[1]/p'
        accept_personal_data_button = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, accept_button_xpath))
        )
        accept_personal_data_button.click()
        time.sleep(0.5)
        logger.info("Accepted personal data policy.")
    except (NoSuchElementException, TimeoutException):
        logger.warning("Accept personal data button not found.")

    try:
        # Wait for and click the language selection button
        language_button = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, 'langSelect-EN'))
        )
        language_button.click()
        time.sleep(0.5)
        logger.info("Language set to English.")
    except (NoSuchElementException, TimeoutException):
        logger.warning("Language selection button not found.")

    # Close footer cookies (if any)
    try:
        accept_cookies_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/a[1]'))
        )
        accept_cookies_button.click()
        time.sleep(0.5)
        logger.info("Accepted footer cookies.")
    except (NoSuchElementException, TimeoutException):
        logger.info("Footer cookies acceptance not required.")

def import_latest_save(driver):
    """
    Imports the latest game save from the exports directory.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    """
    # Read latest export file from EXPORT_PATH
    list_of_files = glob.glob(str(EXPORT_PATH / '*.txt'))
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            save_data = f.read()
        logger.info(f"Imported save from {latest_file}")

        try:
            # Click Options
            options_button = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, 'prefsButton'))
            )
            options_button.click()
            time.sleep(0.5)

            # Click Import Save
            import_save_link = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Import save'))
            )
            import_save_link.click()
            time.sleep(0.5)

            # Paste in textarea
            textarea = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, 'textareaPrompt'))
            )
            textarea.send_keys(save_data)

            # Click Load
            load_button = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, 'promptOption0'))
            )
            load_button.click()
            time.sleep(0.5)

            # Close options
            options_button.click()
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Error during import save: {e}")
    else:
        logger.info("No export files found in EXPORT_PATH.")

def click_golden_cookie(driver):
    """
    Checks for golden cookies and clicks them if found.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    """
    try:
        shimmer_div = driver.find_element(By.XPATH, '//*[@id="shimmers"]//div[contains(@class, "shimmer")]')
        shimmer_div.click()
        logger.info("Clicked a golden cookie.")
    except NoSuchElementException:
        pass  # No golden cookie found
    except Exception as e:
        logger.error(f"Error clicking golden cookie: {e}")

def buy_upgrades_and_products(driver):
    """
    Buys available upgrades and products.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    """
    # Buy upgrades
    try:
        upgrades_panel = driver.find_element(By.ID, 'upgrades')
        enabled_upgrades = upgrades_panel.find_elements(By.CSS_SELECTOR, 'div.enabled')
        for upgrade in enabled_upgrades:
            upgrade.click()
            logger.info("Purchased an upgrade.")
    except Exception as e:
        logger.error(f"Error buying upgrades: {e}")
    
    # Buy products
    try:
        products_panel = driver.find_element(By.ID, 'products')
        enabled_products = products_panel.find_elements(By.CSS_SELECTOR, 'div.product.enabled')
        for product in reversed(enabled_products):  # Buy the most expensive first
            product.click()
            logger.info("Purchased a product.")
    except Exception as e:
        logger.error(f"Error buying products: {e}")

def export_save(driver):
    """
    Exports the current game save to the exports directory.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    """
    try:
        # Click options
        options_button = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, 'prefsButton'))
        )
        options_button.click()

        # Click Export Save
        export_save_link = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Export save'))
        )
        export_save_link.click()

        # Copy content from textarea
        textarea = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, 'textareaPrompt'))
        )
        save_data = textarea.get_attribute('value')

        # Click All done
        all_done_button = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, 'promptOption0'))
        )
        all_done_button.click()

        # Close options
        options_button.click()

        # Save the copied content to the exports dir in a txt file with date-time format
        filename = time.strftime("%Y-%m-%d--%H-%M-%S") + '.txt'
        filepath = EXPORT_PATH / filename
        with open(filepath, 'w') as f:
            f.write(save_data)

        logger.info(f"Game saved to {filepath}")

        # Cleanup old backups
        cleanup_old_backups()
    except Exception as e:
        logger.error(f"Error during export save: {e}")

def cleanup_old_backups():
    """
    Keeps only the latest MAX_BACKUPS files in the exports directory and deletes older ones.
    """
    list_of_files = sorted(glob.glob(str(EXPORT_PATH / '*.txt')), key=os.path.getctime)
    if len(list_of_files) > MAX_BACKUPS:
        files_to_delete = list_of_files[:-MAX_BACKUPS]
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                logger.info(f"Deleted old backup file {file_path}")
            except Exception as e:
                logger.error(f"Could not delete file {file_path}: {e}")

def main():
    """
    Main function to run the Cookie Clicker automation script.
    """
    # Ensure the exports directory exists
    EXPORT_PATH.mkdir(exist_ok=True)
    
    driver = setup_driver()
    driver.get("https://orteil.dashnet.org/cookieclicker/")

    try:
        # Wait for the page to load
        WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "langSelect-EN"))
        )
        accept_cookies_and_select_language(driver)
        
        # Wait until 'bigCookie' is present
        big_cookie = WebDriverWait(driver, WEBPAGE_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        
        # Import latest save if available
        import_latest_save(driver)
        
        logger.info("Starting the Cookie Clicker bot. Press 'Esc' to pause, 'x' to exit.")
        start_time = time.time()
        last_check_time = start_time
        last_export_time = start_time

        while True:
            # Check if 'Esc' is pressed to pause
            if keyboard.is_pressed('esc'):
                logger.info("Paused. Press 'x' to exit, any other key to continue.")
                user_input = input()
                if user_input.lower() == 'x':
                    logger.info("Exiting the script.")
                    break
                else:
                    logger.info("Resuming the bot.")
                    start_time = time.time()
                    last_check_time = start_time
                    last_export_time = start_time
                    continue

            # Click golden cookies if any
            click_golden_cookie(driver)
            
            # Click the big cookie
            big_cookie.click()
            time.sleep(COOKIE_CLICK_DELAY)
            
            current_time = time.time()

            # Every 'CHECK_INTERVAL' seconds, check for upgrades and products
            if current_time - last_check_time >= CHECK_INTERVAL:
                buy_upgrades_and_products(driver)
                last_check_time = current_time

            # Every 'EXPORT_INTERVAL' seconds, export the game save
            if current_time - last_export_time >= EXPORT_INTERVAL:
                export_save(driver)
                last_export_time = current_time

    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
