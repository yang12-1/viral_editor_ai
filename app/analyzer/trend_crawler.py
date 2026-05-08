from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def crawl_tiktok_trends():

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )

    driver.get("https://www.tiktok.com/trending")

    time.sleep(5)

    trends = []

    elements = driver.find_elements(By.TAG_NAME, "h3")

    for e in elements[:10]:
        trends.append(e.text)

    driver.quit()

    return trends
