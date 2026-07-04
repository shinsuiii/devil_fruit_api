import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC



def main():
    root_url = "https://onepiece.fandom.com/wiki/Paramecia"
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)  # fail fast instead of hanging 120s
    
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

        # Iterates through the list of sortable jquery-tablesorter; in paramecia wiki, there are nine (9) of these tables
        for table in tables:
            # "tbody tr" is combined assuming there is only ONE tbody inside each table
            tr_list = table.find_elements(By.CSS_SELECTOR, "tbody tr")

            for tr in tr_list:
                # td == all td tags inside a tr; it is a list of tds
                td = tr.find_elements(By.TAG_NAME, "td")
                anchor = td[1].find_elements(By.CSS_SELECTOR, "a")
                span_element = td[1].find_elements(By.TAG_NAME, "span")

                try:
                    if span_element:
                        if len(anchor) == 1:
                            previous_user = anchor[0].text
                        else:
                            previous_user = anchor[0].text
                            user = anchor[1].text
                    else:
                        user = anchor[0].text

                except IndexError:
                    print(f"Missing user for {td[0].find_element(By.TAG_NAME, 'a').text}")

                id_counter += 1

                data = {
                    "id": f"{id_counter}",
                    "name": td[0].find_element(By.TAG_NAME, "a").text,
                    **({"user": user} if ((span_element and len(anchor) > 1) or (not span_element)) else {}),
                    **({"previous_user": previous_user} if span_element else {}),
                    "type": "Paramecia",
                    "canon_status": before_ref if table == reference_table else after_ref,
                    "description": td[2].text if len(td) > 2 else "",
                }
                data_storage.append(data)
                time.sleep(0.2)

    finally:
        driver.quit()
        with open("expanded_data.json", "w") as file:
            json.dump(data_storage, file, indent=2)



if __name__ == "__main__":
    main()