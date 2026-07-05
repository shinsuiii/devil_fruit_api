import json
import time
import requests
from selectolax.lexbor import LexborHTMLParser



def main():
    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/149.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    }

    combined_info = []
    id_counter = 0

    type_counter = 0
    type_convert = {
        "1": "Paramecia",
        "2": "Logia",
        "3": "Zoan",
    }

    root_url = ["https://onepiece.fandom.com/wiki/Paramecia", "https://onepiece.fandom.com/wiki/Logia", "https://onepiece.fandom.com/wiki/Zoan"]
    for url in root_url:
        texts, counter = get_df_info(url, headers, id_counter)
        id_counter += counter

        df_links = get_links(url, headers)
        images = get_img_src(df_links, headers)

        combined_info.append(d1 | d2 for d1, d2 in zip(texts, images))
        time.sleep(1)

        type_counter += 1
        print(f"{type_convert[str(type_counter)]} webpage is extracted.")

    with open("data.json", "w") as file:
        json.dump(combined_info, file, indent=2)


def get_df_info(url, headers, id_counter):
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)
    tree = LexborHTMLParser(response.text)

    id_counter = id_counter

    text_data = []

    tables = tree.css(".sortable")
    ref_table = tree.css_first(".sortable")

    for table in tables:
        tbody = table.css_first("tbody")
        tr_list = tbody.css("tr")

        for tr in tr_list:
            td = tr.css("td")
            if not td:
                continue
            if not td[0].css_first("small") in td[0]:
                en_name = None
            else: # Sets and cleans the English name
                raw_en_name = td[0].css_first("small").text()
                en_name = raw_en_name.replace("(", "").replace(")", "").replace(";", "; ").strip()
            
            prev_user = None
            current_user = None
            span = None
            anchor = []
            if td[1].css_first("span") in td[1]:
                span = td[1].css_first("span")
                anchor = td[1].css("a")
                if len(anchor) == 1:
                    prev_user = anchor[0].text()
                else:
                    prev_user = anchor[0].text()
                    current_user = anchor[1].text()
            else:
                current_user = td[1].css_first("a").text()

            id_counter += 1
            data = {
                    "id": str(id_counter),
                    "name": td[0].css_first("a").text(),
                    **({"en_name": en_name} if en_name else {}),
                    **({"user": current_user} if (not span) or (len(anchor) != 1) else {}),
                    **({"previous_user": prev_user} if span else {}),
                    "type": f'{url.replace("https://onepiece.fandom.com/wiki/", "")}',
                    "canon_status": "Canon" if table == ref_table else "Non-Canon",
                    "description": td[2].text() if len(td) > 2 else "",
            }
            text_data.append(data)

    return text_data, id_counter


def get_links(url, headers):
    response = requests.get(url, headers=headers)
    tree = LexborHTMLParser(response.text)

    df_links = []

    tables = tree.css(".sortable")    
    for table in tables:
        tbody = table.css_first("tbody")
        tr_list = tbody.css("tr")
        for tr in tr_list:
            td_list = tr.css("td")
            # Skips <th> tags
            if not td_list:
                continue

            df_link_td = td_list[0]
            a_element = df_link_td.css_first("a")

            try:
                link = "https://onepiece.fandom.com" + a_element.attributes.get("href")
                data = {
                    "df_link": link
                }
                df_links.append(data)
            except AttributeError:
                print("Missing attribute")
                continue

    return df_links


def get_img_src(df_links, headers):
    img_srcs = []

    session = requests.Session()
    session.headers.update(headers)

    for link in df_links:
        url = link["df_link"]
        response = session.get(url)
        tree = LexborHTMLParser(response.text)

        figure = tree.css(".pi-item.pi-image")
        anchor = figure[0].css_first("a")
        img = anchor.css_first("img")

        data = {
            "img_src": img.attributes.get("src")
        }
        img_srcs.append(data)
        time.sleep(0.5)

    return img_srcs



if __name__ == "__main__":
    main()