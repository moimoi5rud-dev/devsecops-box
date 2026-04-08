import sqlite3

def login(username, password):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    # Lỗ hổng SQL Injection ở đây
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    return cursor.fetchone()

print("Vulnerable code ready for Cline to fix")
