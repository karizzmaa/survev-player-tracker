import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get("https://survev.io/")
        wait = WebDriverWait(driver, 20)
        select_element = wait.until(EC.presence_of_element_located((By.ID, "server-select-main")))
        time.sleep(5)
        
        options = select_element.find_elements(By.TAG_NAME, "option")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_rows = []
        
        for option in options:
            text = option.text
            if "[" in text and "]" in text:
                server_name = text.split("[")[0].strip()
                player_count = text.split("[")[1].split("]")[0].replace(" players", "").strip()
                data_rows.append([timestamp, server_name, player_count])

        with open("latest.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Server", "Players"])
            writer.writerows(data_rows)

        with open("old.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([])
            writer.writerow([f"--- RUN AT {timestamp} ---"])
            writer.writerow(["Timestamp", "Server", "Players"])
            writer.writerows(data_rows)
            
        for row in data_rows:
            print(f"{row[0]} | {row[1].ljust(15)} | {row[2]} players")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape()
