import sqlite3
import string
import random
import re


# Initialize Database Table
def init_db():
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                url TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

def add(code: str, url: str):
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (code, url) VALUES (?, ?)", (code, url))

def getallcodes():
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code FROM urls")
        return {row[0] for row in cursor.fetchall()}

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


url_pattern = re.compile(r"^(https://|https?://[\w.-]+\.[a-zA-Z]{2,})")
not_prefix = re.compile(r"^[\w.-]+\.[a-zA-Z]{2,}")

def validate_url(input):
    if bool(url_pattern.match(input)) == False:
        if bool(not_prefix.match(input)) == True:
            new_url = "https://"+input
            return new_url
        else:
            return "Error 7: Invalid Url Format"
    else:
        return input