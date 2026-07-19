import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    skills TEXT
)
""")

# Internships Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS internships(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    location TEXT NOT NULL,
    stipend TEXT NOT NULL,
    duration TEXT NOT NULL
)
""")

# Applications Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    internship_id INTEGER,
    status TEXT DEFAULT 'Applied',
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(internship_id) REFERENCES internships(id)
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")