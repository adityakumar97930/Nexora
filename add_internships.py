import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

internships = [

("Google", "Frontend Developer", "Bangalore", "₹30,000/month", "3 Months"),

("Microsoft", "Python Developer", "Hyderabad", "₹35,000/month", "6 Months"),

("Amazon", "Cloud Intern", "Remote", "₹40,000/month", "6 Months"),

("IBM", "AI Intern", "Pune", "₹25,000/month", "4 Months"),

("Infosys", "Data Analyst", "Noida", "₹22,000/month", "6 Months"),

("TCS", "Cyber Security Intern", "Chennai", "₹28,000/month", "6 Months")

]

cursor.executemany("""

INSERT INTO internships(company, role, location, stipend, duration)

VALUES(?,?,?,?,?)

""", internships)

conn.commit()
conn.close()

print("Internships Added Successfully!")