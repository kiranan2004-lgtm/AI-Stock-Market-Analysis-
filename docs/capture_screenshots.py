import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def capture_all():
    os.makedirs('screenshots', exist_ok=True)
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--window-size=1440,960')
    opts.add_argument('--force-device-scale-factor=1.2')
    driver = webdriver.Chrome(options=opts)

    try:
        print("1. Capturing login page...")
        driver.get('http://127.0.0.1:8000/login/')
        time.sleep(1.5)
        driver.save_screenshot('screenshots/login_page.png')
        print(" -> Saved screenshots/login_page.png")

        print("Logging in as demo_trader...")
        driver.find_element(By.NAME, 'username').send_keys('demo_trader')
        driver.find_element(By.NAME, 'password').send_keys('StockSense@2026')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2.5)

        print("2. Capturing dashboard...")
        driver.save_screenshot('screenshots/stock_dashboard.png')
        print(" -> Saved screenshots/stock_dashboard.png")

        print("3. Capturing stock chart / explorer...")
        driver.get('http://127.0.0.1:8000/stocks/TCS.NS/')
        time.sleep(2.5)
        driver.save_screenshot('screenshots/stock_chart.png')
        print(" -> Saved screenshots/stock_chart.png")

        print("4. Capturing ML forecasting...")
        driver.get('http://127.0.0.1:8000/predictions/?symbol=TCS.NS')
        time.sleep(2.5)
        driver.save_screenshot('screenshots/ml_forecasting.png')
        print(" -> Saved screenshots/ml_forecasting.png")

        print("5. Capturing news sentiment analysis...")
        driver.get('http://127.0.0.1:8000/news/?symbol=TCS.NS')
        time.sleep(2.5)
        driver.save_screenshot('screenshots/news_sentiment.png')
        print(" -> Saved screenshots/news_sentiment.png")

        print("All screenshots successfully captured!")
    finally:
        driver.quit()

if __name__ == '__main__':
    capture_all()
