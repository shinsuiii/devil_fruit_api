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
    expanded_data = []
    id_counter = 0

    driver = webdriver.Chrome()

    try:
        driver.get(root_url)
        root_table = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sortable.jquery-tablesorter"))
        )

        for table in root_table:
            target_row = table.find_elements(By.CSS_SELECTOR, "tbody")

            for row in target_row:
                id_counter += 1

                try:
                    fruit_user = row.find_element(By.XPATH, ".//td[2]")
                    span_indicator = fruit_user.find_element(By.CSS_SELECTOR, ".nomobile")
                    # Checks the existence of a previous user.
                    if span_indicator:
                        previous_user = fruit_user.find_element(By.XPATH, ".//a[1]").text
                        current_user = fruit_user.find_element(By.XPATH, ".//a[2]").text
                    else:
                        current_user = fruit_user.find_element(By.XPATH, ".//a[1]").text
                except NoSuchElementException:
                    pass

                data = {
                    "id": id_counter,
                    "name": row.find_element(By.XPATH, ".//td[1]/a").text,
                    "type": root_url.replace("https://onepiece.fandom.com/wiki/", ""),
                    "current_user": current_user,
                    **({"previous_user": previous_user}),
                    "description": row.find_element(By.XPATH, ".//td[3]").text,
                }

                expanded_data.append(data)
                time.sleep(0.1)
            
            id_counter = 0 # resets counter to zero after iterating through a tabl
            time.sleep(0.1)
        
        with open("expanded_data.json", "w") as file:
            json.dump(expanded_data, file, indent=2)
    
    except TimeoutException:
        driver.quit()

    driver.quit()


def test():
    root_url = "https://onepiece.fandom.com/wiki/Paramecia"
    driver = webdriver.Chrome()

    driver.get(root_url)
    table_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sortable.jquery-tablesorter"))
    )

    print(len(table_list))

    driver.quit()





if __name__ == "__main__":
    main()