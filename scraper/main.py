import json
import time
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
        tables = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sortable.jquery-tablesorter"))
        )
        
        # Determines if a df is canon or non-canon
        reference_table = tables[0]
        before_ref = reference_table.find_element(By.XPATH, "./preceding-sibling::h3[1]/span[1]").text
        after_ref = reference_table.find_element(By.XPATH, "./following-sibling::h3[1]/span[1]").text

        # Iterates through the list of sortable jquery-tablesorter
        # In paramecia wiki, there are nine (9) of these tables
        for table in tables:
            tbody = table.find_elements(By.TAG_NAME, "tbody")

            for body in tbody:
                tr_list = body.find_elements(By.TAG_NAME, "tr")

                for tr in tr_list:
                    # td == all td tags inside a tr
                    td = tr.find_elements(By.TAG_NAME, "td")
                    id_counter += 1

                    data = {
                        "id": f"{id_counter}",
                        "name": td[0].find_element(By.TAG_NAME, "a").text,
                        "type": "Paramecia",
                        "canon_status": before_ref if table == reference_table else after_ref,
                        "description": td[2].text if len(td) > 2 else "",
                    }

                    data_storage.append(data)
                    time.sleep(0.2)

                time.sleep(0.2)

            time.sleep(0.2)

    except TimeoutException:
        driver.quit()

    with open("expanded_data.json", "w") as file:
        json.dump(data_storage, file, indent=2)

    driver.quit()



if __name__ == "__main__":
    main()