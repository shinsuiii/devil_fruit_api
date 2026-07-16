CREATE TABLE devil_fruits (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    en_name TEXT,
    type TEXT,
    user_name TEXT,
    previous_user TEXT,
    canon_status TEXT,
    description TEXT,
    appears_in TEXT,
    img_src TEXT
);

CREATE TABLE zoan_specific (
    zoan_id INTEGER PRIMARY KEY,
    series TEXT,
    sub_type TEXT,

    FOREIGN KEY (zoan_id)
        REFERENCES devil_fruits(id)
);