import json
import time
from selectolax.lexbor import LexborHTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



def main():
    driver = webdriver.Chrome()

    root_url = "https://onepiece.fandom.com/wiki/Paramecia"
    root_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".sortable.jquery-tablesorter"))
    )

    urls = get_links(driver, root_url, root_table)
    
    data_list = []

    try:
        driver.get(root_url)


        main_table = root_table.find_elements(By.CSS_SELECTOR, "tbody tr")

        for table in main_table:
            data = {
                "name": table.find_element(By.XPATH, ".//td[1]/a").text,
                "user": table.find_element(By.XPATH, ".//td[2]/a").text,
                "description": table.find_element(By.XPATH, ".//td[3]").text,
            }

            data_list.append(data)
            time.sleep(0.2)

    except TimeoutException:
        driver.quit()
    
    with open("data.json", "w") as file:
        json.dump(data_list, file, indent=2)

    driver.quit()



def get_links(driver, root_url, root_table):
    try:
        driver.get(root_url)

        

        




    except TimeoutException:
        driver.quit()












if __name__ == "__main__":
    main()