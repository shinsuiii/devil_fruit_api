import requests
from selectolax.lexbor import LexborHTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



def main():
    driver = webdriver.Chrome()
    urls = get_links("https://onepiece.fandom.com/wiki/Paramecia", driver)
    print(urls)





def get_links(root_url, driver):
    driver.get(root_url)
    table_row = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(By.CSS_SELECTOR, ".sortable.jquery-tablesorter")
    )

    urls = []

    for table in table_row:
        urls.append(table.css_first("tbody tr td a").attributes.get("href"))

    driver.quit()
    return urls
    ...


def scrape():

    ...








def test_1():
    url = "https://onepiece.fandom.com/wiki/Paramecia"
    
    driver = webdriver.Chrome()
    driver.get(url)

    cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(By.CSS_SELECTOR, "")
    )

    for card in cards:
        data = {

        }

    driver.quit()


def test_2():
    url = "https://onepiece.fandom.com/wiki/Paramecia"

    driver = webdriver.Chrome()
    driver.get(url)

    tables = driver.find_elements(By.CSS_SELECTOR, "")

    # Searches only what is inside the container inside "tables" (tables == WebElement)
    for table in tables:
        name = table.find_element(By.CSS_SELECTOR, "")


    print(driver.title)

    driver.quit()



def get_img_src():
    url = "https://onepiece.fandom.com/wiki/Paramecia"
    driver = webdriver.Chrome()
    driver.get(url)

    img = driver.find_element(By.TAG_NAME, "img")

    src = img.get_attribute("src")
    print(src)

    driver.quit()



if __name__ == "__main__":
    main()