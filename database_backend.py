import sqlite3
import string
import random

# Initialize Database Table
def init_db():
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL,
                url TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

def add(code: str, url: str):
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (code, url) VALUES (?, ?)", (code, url))

def get_all_data():
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code, url FROM urls")
        return cursor.fetchall()

def search(target: str):
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        # COLLATE NOCASE makes the search case-insensitive
        cursor.execute(
            "SELECT code, url FROM urls WHERE code = ? COLLATE NOCASE OR url = ? COLLATE NOCASE", 
            (target, target)
        )
        result = cursor.fetchone()
        
        if result:
            return {"code": result[0], "url": result[1]}
        return None


def gen_code():
    alphanumericlist = string.ascii_uppercase + string.digits
    all_codes = getallcodes()
    
    while True:
        code = "".join(random.choices(alphanumericlist, k=5))
        if code not in all_codes:
            return code

    

def getallcodes():
    data = get_all_data()
    for i in range(len(data)):
        return(data[0][i])