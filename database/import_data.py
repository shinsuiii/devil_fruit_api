import json
import psycopg



def main():
    conn = psycopg.connect(
        host="localhost",
        dbname="df_db",
        user="postgres",
        password="shanejoey21",
        port=5432,
    )

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

    with conn:
        with conn.cursor() as cur:
            cur.executemany(query, rows)

    print(f"Inserted {len(rows)} fruits!")



if __name__ == "__main__":
    main()