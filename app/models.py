from create_database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
Create table User(
               id INT PRIMARY KEY IDENTITY(1,1),
               username VARCHAR(100),
               email Varchar(100),
               password varchar(255))
""")

conn.commit()
conn.close()