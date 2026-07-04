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
    df_links = get_links()
    img_srcs = get_img_src(df_links)

    root_url = "https://onepiece.fandom.com/wiki/Paramecia"
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)  # Fail fast instead of hanging 120s
    
    text_data = []
    id_counter = 0

    try:
        driver.get(root_url)
        tables = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sortable.jquery-tablesorter"))
        )
        
        reference_table = tables[0] # Determines if a df is canon or non-canon
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
                text_data.append(data)
                time.sleep(0.2)

    finally:
        driver.quit()
        # Combines the text data with the images src link extracted
        data_storage = [text_data | img_srcs for text_data, img_srcs in zip(text_data, img_srcs)]
        with open("data.json", "w") as file:
            json.dump(data_storage, file, indent=2)


def get_links():
    root_url = "https://onepiece.fandom.com/wiki/Paramecia"
    options = Options()
    options.page_load_strategy = "normal"
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--blink-settings=imagesEnabled=false")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(90)
    driver.set_script_timeout(90)

    df_links = []

    try:
        driver.get(root_url)
        time.sleep(2)
        tables = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sortable.jquery-tablesorter"))
        )

        for table in tables:
            tr_list = table.find_elements(By.CSS_SELECTOR, "tbody tr")

            for tr in tr_list:
                td = tr.find_elements(By.TAG_NAME, "td")

                try:
                    link = td[0].find_element(By.TAG_NAME, "a").get_attribute("href")
                except NoSuchElementException:
                    print("No link...")

                data = {"fruit_link": link,}
                df_links.append(data)
                time.sleep(0.2)

    finally:
        driver.quit()
        print("Links successfully extracted.")

    return df_links


def get_img_src(df_links):
    options = Options()
    options.page_load_strategy = "eager"
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--blink-settings=imagesEnabled=false")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(90)
    driver.set_script_timeout(90)

    img_srcs = []

    try:
        for link in df_links:
                driver.get(link["fruit_link"])
                figure_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".pi-item.pi-image"))
                )

                for figure in figure_element:
                    try:
                        img = figure.find_element(By.CSS_SELECTOR, ".image.image-thumbnail img").get_attribute("src")
                        data = {"img_src": img,}
                        img_srcs.append(data)

                    except TimeoutException:
                        print(f"No image found for {link['fruit_link']}")
                        img_srcs.append({"img_src": None})
    finally:
        driver.quit()

    print("Image sources extracted successfully.")
    return img_srcs



if __name__ == "__main__":
    main()