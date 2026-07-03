import json
import time
from selectolax.lexbor import LexborHTMLParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC



def main():
    root_url = "https://onepiece.fandom.com/wiki/Paramecia"
    driver = webdriver.Chrome()
    data_storage = []
    id_counter = 0

    try:
        driver.get(root_url)
        table_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sortable.jquery-tablesorter"))
        )
        
        for table in table_list:
            # Gets all tbody (9)
            target_row = table.find_elements(By.TAG_NAME, "tbody")

            # Determines if a df is canon or non-canon
            reference_table = table_list[0]
            before_ref = reference_table.find_element(By.XPATH, "./preceding-sibling::h3[1]/span[1]").text
            after_ref = reference_table.find_element(By.XPATH, "./following-sibling::h3[1]/span[1]").text

            for row in target_row:
                # Gets all tr inside a tbody
                tr = row.find_elements(By.TAG_NAME, "tr")

                for td in tr:
                    id_counter += 1
                    data = {
                        "id": f"{id_counter}",
                        "name": td.find_element(By.XPATH, ".//td[1]/a").text,
                        "type": "Paramecia",
                        "canon_status": before_ref if table == reference_table else after_ref,
                        "description": td.find_element(By.XPATH, ".//td[3]").text,
                    }

                    data_storage.append(data)
                    time.sleep(0.2)

            time.sleep(0.2)

    except TimeoutException:
        driver.quit()

    with open("data.json", "w") as file:
        json.dump(data_storage, file, indent=2)

    driver.quit()



if __name__ == "__main__":
    main()