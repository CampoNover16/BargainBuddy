from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import pyshorteners

def OLXDislayItems(page_link, demand_item_name, item_category_name):
    start_time = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()

    driver.get(page_link)
    driver.implicitly_wait(10)

    time.sleep(1)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    driver.find_element(By.ID, "search").send_keys(demand_item_name)

    driver.find_element(By.CSS_SELECTOR, '[data-testid="search-submit"]').click()
    time.sleep(3)

    dropdown_category = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cy='category-dropdown']")))
    dropdown_category.click()
    time.sleep(1)

    child_xpath_expression = f"//*[span[text()='{item_category_name}']]"
    child_element = driver.find_element(By.XPATH, child_xpath_expression)

    parent_xpath_expression = f"{child_xpath_expression}/parent::*"
    parent_element = child_element.find_element(By.XPATH, parent_xpath_expression)

    time.sleep(1)

    category_id = parent_element.get_attribute("data-categoryid")

    item_category = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[data-categoryid='{category_id}']")))
    item_category.click()

    time.sleep(1)
    dropdown_sort = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-u2fqob")))
    dropdown_sort.click()

    item_sort_xpath = f"//*[contains(text(), 'Czas: Najnowsze')]"

    item_sort = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, item_sort_xpath)))
    item_sort.click()

    time.sleep(2)
    all_elements = driver.find_elements(By.CSS_SELECTOR, "[data-cy='l-card']")

    formatted_data = []
    #type_tiny = pyshorteners.Shortener()

    for result in all_elements[:15]:
        #href = result.find_element(By.CLASS_NAME, "css-rc5s2u").get_attribute('href') if result.find_elements(By.CLASS_NAME, "css-rc5s2u") else "-"
        title = result.find_element(By.TAG_NAME, "h6").text if result.find_elements(By.TAG_NAME, "h6") else "-"
        cost = result.find_element(By.CSS_SELECTOR, '[data-testid="ad-price"]').text if result.find_elements(By.CSS_SELECTOR, '[data-testid="ad-price"]') else "-"
        place = result.find_element(By.CSS_SELECTOR, '[data-testid="location-date"]').text if result.find_elements(By.CSS_SELECTOR, '[data-testid="location-date"]') else "-"
        status = result.find_element(By.CLASS_NAME, 'css-3lkihg').text if result.find_elements(By.CLASS_NAME, 'css-3lkihg') else "-"
        # if cost and float((cost.split(" zł")[0]).replace(',','.').replace(' ', '')) < 50.00:
        #     continue

        #short_url = type_tiny.tinyurl.short(href)

        formatted_data.append([title, cost, place, status])
        #formatted_data.append([title, cost, place, status, short_url])

    headers = ["Title", "Cost", "Place", "Stat"]
    #headers = ["Title", "Cost", "Place", "Stat", "Link"]

    table = tabulate(formatted_data, headers=headers, tablefmt="pretty")

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    end_time = time.time()
    running_time = end_time - start_time

    print(f"Scanning time: {round(running_time,2)} sec")
    print("Scanned at:", formatted_time)
    print(table)

    next_scan_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    formatted_scan_time = next_scan_time.strftime('%Y-%m-%d %H:%M:%S')

    print(f"Next scan: {formatted_scan_time}")

    time.sleep(1)
    driver.close()


while(True):
    OLXDislayItems('https://www.olx.pl/', 'Wiedźmin stary świat', 'Sport i Hobby')
    time.sleep(15*60)
