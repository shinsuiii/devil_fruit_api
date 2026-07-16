import json
import psycopg



def main():
    connect = psycopg.connect(
        host="localhost",
        dbname="df_db",
        user="postgres",
        password="shanejoey21",
        port=5432,
    )

    with connect:
        query, rows = devil_fruits()
        with connect.cursor() as cursor:
            cursor.executemany(query, rows)
        
        zoan_query, zoan_rows = zoan_specific()
        with connect.cursor() as cursor:
            cursor.executemany(zoan_query, zoan_rows)

    print(f"Inserted fruits!")


def devil_fruits():
    query = """
    INSERT INTO devil_fruits (
        id,
        name,
        en_name,
        type,
        user_name,
        previous_user,
        canon_status,
        description,
        appears_in,
        img_src
    )
    VALUES (
        %(id)s,
        %(name)s,
        %(en_name)s,
        %(type)s,
        %(user_name)s,
        %(previous_user)s,
        %(canon_status)s,
        %(description)s,
        %(appears_in)s,
        %(img_src)s
    )
    ON CONFLICT (id) DO NOTHING;
    """

    with open("../scraper/data.json", "r", encoding="utf-8") as file:
        fruits = json.load(file)

    rows = [
        {
            "id": int(fruit["id"]),
            "name": fruit.get("name"),
            "en_name": fruit.get("en_name"),
            "type": fruit.get("type"),
            "user_name": fruit.get("user"),
            "previous_user": fruit.get("previous_user"),
            "canon_status": fruit.get("canon_status"),
            "description": fruit.get("description"),
            "appears_in": fruit.get("appears_in"),
            "img_src": fruit.get("img_src"),
        }
        for fruit in fruits
    ]
    return query, rows


def zoan_specific():
    query = """
    INSERT INTO zoan_specific (
        zoan_id,
        series,
        sub_type
    )
    VALUES (
        %(zoan_id)s,
        %(series)s,
        %(sub_type)s
    )
    ON CONFLICT (zoan_id) DO NOTHING;
    """

    with open("../scraper/data.json", "r", encoding="utf-8") as file:
        fruits = json.load(file)

    rows = [
        {
            "zoan_id": int(fruit["id"]),
            "series": None if fruit.get("series") == "Unknown" else fruit.get("series"),
            "sub_type": None if fruit.get("sub-type") == "Unknown" else fruit.get("sub-type"),
        }
        for fruit in fruits
        if fruit.get("type") == "Zoan"
    ]
    return query, rows



if __name__ == "__main__":
    main()