from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random, os

def setup_driver():
    options = webdriver.ChromeOptions()
    user_data_dir = os.path.abspath("User_Data")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(executable_path=os.path.abspath("chromedriver.exe"))
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://web.whatsapp.com")
    print("🔄 Waiting for WhatsApp Web login...")

    try:
        WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.ID, "side"))
        )
        print("✅ Logged in successfully!")
    except:
        print("❌ Login timeout. Please scan the QR code.")
        input("Press Enter to quit...")
        driver.quit()
        exit()

    return driver

def send_message(driver, number, message):
    url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
    driver.get(url)
    print(f"📨 Opening chat for {number}")
    sleep(random.randint(8, 12))

    try:
        send_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        send_btn.click()
        print(f"✅ Sent to {number}")
        return True
    except Exception as e:
        print(f"❌ Failed for {number}: {e}")
        return False
