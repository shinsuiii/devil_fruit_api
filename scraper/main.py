import requests
from selectolax.lexbor import LexborHTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



def main():
    url = "https://onepiece.fandom.com/wiki/Paramecia"
    response = requests.get()

    options = Options()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(By.CSS_SELECTOR, "")
    )

    html = driver.page_source
    driver.quit()

    tree = LexborHTMLParser(html)



def test():
    url = "https://onepiece.fandom.com/wiki/Paramecia"

    driver = webdriver.Chrome()
    driver.get(url)

    tables = driver.find_elements(By.CSS_SELECTOR, "")

    # Searches only what is inside the container inside "tables"
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
    test()
    #main()