import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=CustomerReviewDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

cursor.execute("SELECT name FROM sys.databases")

cursor.execute("SELECT * FROM Users")

# cursor.execute("SELECT * FROM CustomerReviews ")



for row in cursor.fetchall():
    print(row)

conn.close()