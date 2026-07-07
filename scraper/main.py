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
    session = requests.Session()
    session.headers.update(headers)

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
        if root_url[2] == url:
            texts, id_counter = get_zoan_info(url, session, id_counter)
        else:
            texts, id_counter = get_df_info(url, session, id_counter)
        df_links = get_links(url, headers)
        images = get_img_src(df_links, session)
        
        type_counter += 1
        print(f"{type_convert[str(type_counter)]} webpage is extracted.")
        combined_info.extend(d1 | d2 for d1, d2 in zip(texts, images))
        time.sleep(0.5)

    with open("data.json", "w") as file:
        json.dump(combined_info, file, indent=2)


def get_df_info(url, session, id_counter):
    response = session.get(url)
    html = response.text.replace("<br>", "; ").replace("<br/>", "; ").replace("<br />", "; ")
    tree = LexborHTMLParser(html)

    status_code = response.status_code
    print(status_code)

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
                    "name": clean(td[0].css_first("a").text()),
                    **({"en_name": clean(en_name)} if en_name else {}),
                    "type": f'{url.replace("https://onepiece.fandom.com/wiki/", "")}',
                    **({"user": clean(current_user)} if (not span) or (len(anchor) != 1) else {}),
                    **({"previous_user": clean(prev_user)} if span else {}),
                    "canon_status": "Canon" if table == ref_table else "Non-Canon",
                    "description": clean(td[2].text()) if len(td) > 2 else "",
            }
            text_data.append(data)
    return text_data, id_counter


def get_zoan_info(url, session, id_counter):
    response = session.get(url)
    html = response.text.replace("<br>", "; ").replace("<br/>", "; ").replace("<br />", "; ")
    tree = LexborHTMLParser(html)

    status_code = response.status_code
    print(status_code)

    id_counter = id_counter
    text_data = []

    tables = tree.css(".sortable")
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
            span = td[1].css("span")
            anchor = []
            if len(td) > 3:
                if span in td[1]:
                    anchor = td[1].css("a")
                    if len(anchor) == 1:
                        prev_user = anchor[0].text()
                    else:
                        prev_user = anchor[0].text()
                        current_user = anchor[1].text()
                else:
                    current_user = td[1].css_first("a").text()
            if anchor:
                name = td[0].css_first("a").text()
            else:
                name = td[0].text()
                if name == "Unknown\n" or name == None:
                    continue
            
            id_counter += 1
            if len(td) > 3:
                data = {
                        "id": str(id_counter),
                        "name": clean(name),
                        **({"en_name": clean(en_name)} if en_name else {}),
                        "type": f'{url.replace("https://onepiece.fandom.com/wiki/", "")}',
                        "series": clean(td[2].css_first("a").text()) if anchor else clean(td[2].text()),
                        "sub-type": clean(td[3].css_first("a").text()) if anchor else clean(td[3].text()),
                        **({"user": clean(current_user)} if (not span) or (len(anchor) != 1) else {}),
                        **({"previous_user": clean(prev_user)} if span else {}),
                        "canon_status": "Non-Canon" if table == tables[2] else "Canon",
                        "description/transforms_into": clean(td[4].text()),
                }
            else:
                data = {
                    "id": str(id_counter),
                    "name": clean(f"Unnamed; {td[0].text()}"),
                    "sub-type": clean(td[1].text()),
                    "canon_status": "Canon",
                    "description/transforms_into": clean(td[2].text()),
                }
            text_data.append(data)
    return text_data, id_counter


def get_links(url, headers):
    response = requests.get(url, headers=headers)
    html = response.text.replace("<br>", "; ").replace("<br/>", "; ").replace("<br />", "; ")
    tree = LexborHTMLParser(html)

    status_code = response.status_code
    print(status_code)

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
                continue
    return df_links


def get_img_src(df_links, session):
    img_srcs = []

    for link in df_links:
        url = link["df_link"]
        response = session.get(url)
        html = response.text.replace("<br>", "; ").replace("<br/>", "; ").replace("<br />", "; ")
        tree = LexborHTMLParser(html)

        figure = tree.css(".pi-item.pi-image")
        anchor = figure[0].css_first("a")
        img = anchor.css_first("img")

        data = {
            "img_src": img.attributes.get("src")
        }
        img_srcs.append(data)
        time.sleep(0.2)
    return img_srcs


def clean(text):
    if text is None:
        return None

    cleaned = " ".join(text.replace("/", " ").replace(".;", "; ").replace(";;", ";").replace("; ; ", "; ").split())
    return cleaned


if __name__ == "__main__":
    main()