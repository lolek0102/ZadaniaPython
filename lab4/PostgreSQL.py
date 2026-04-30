import sqlite3
import requests

response = requests.get("https://randomuser.me/api/?results=30")
users = response.json()["results"]

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    age INTEGER,
    gender TEXT,
    country TEXT
)
""")

cur.execute("DELETE FROM Users")

for user in users:
    cur.execute("""
    INSERT INTO Users (first_name, last_name, email, age, gender, country)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user["name"]["first"],
        user["name"]["last"],
        user["email"],
        user["dob"]["age"],
        user["gender"],
        user["location"]["country"]
    ))

conn.commit()

print("Liczba użytkowników wg płci:")
cur.execute("""
SELECT gender, COUNT(*) 
FROM Users 
GROUP BY gender
""")
for row in cur.fetchall():
    print(row)

print("\nŚredni wiek:")
cur.execute("""
SELECT AVG(age) 
FROM Users
""")
print(cur.fetchone()[0])

print("\nLiczba użytkowników wg kraju:")
cur.execute("""
SELECT country, COUNT(*) 
FROM Users 
GROUP BY country 
ORDER BY COUNT(*) DESC
""")
for row in cur.fetchall():
    print(row)

conn.close()