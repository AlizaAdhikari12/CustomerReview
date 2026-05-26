import pyodbc
import os
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_SERVER = os.getenv("DB_SERVER")
DB_DRIVER = os.getenv("DB_DRIVER")

#for connection
def get_connection():
    return pyodbc.connect(
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;",
        autocommit=True
    )

#for database

def create_database():
    conn = pyodbc.connect(
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE=master;"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;",
        autocommit=True

        )
    cursor = conn.cursor()

    cursor.execute(f"""
    IF NOT EXISTS(
               SELECT name FROM sys.databases
               WHERE name ='{DB_NAME}'
               )
               BEGIN
                CREATE DATABASE {DB_NAME}
               END
               """)

    print("database create sucessfully")

    conn.close()

# create tabele

def create_table():
    conn = get_connection()
    cursor = conn.cursor()


    #creating user table
    cursor.execute(f"""
    IF NOT EXISTS(
                   SELECT * FROM sysobjects
                  WHERE name='Users' AND xtype='U'
    )
    CREATE TABLE Users(
        id INT Identity(1,1) PRIMARY KEY,
        FullName NVARCHAR(100) NOT NULL,
        Email NVARCHAR(100) NOT NULL UNIQUE,
        PasswordHash NVARCHAR(255) NOT NULL,
        Role NVARCHAR(20) NOT NULL CHECK (Role IN ('Admin','User')),
        CreateDate DATETIME DEFAULT GETDATE()
    )""")


    #creating revuew table
    cursor.execute(f"""
    IF NOT EXISTS(
        SELECT * FROM sysobjects
        WHERE name = 'CustomerReviews' AND xtype='U'
    )
    CREATE TABLE CustomerReviews (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        UserId INT NOT NULL,
        CustomerName NVARCHAR(100) NOT NULL,
        ReviewText NVARCHAR(MAX) NOT NULL,
        Sentiment NVARCHAR(50),
        Score FLOAT,
        Keywords NVARCHAR(MAX),
        Category NVARCHAR(100),
        AiSummary NVARCHAR(MAX),
        CreateDate DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_CustomerReviews_Users FOREIGN KEY (UserId) REFERENCES Users(id)
    )""")

    conn.commit()
    conn.close()
    print("Table created")

#run everything

if __name__ == "__main__":
    create_database()
    create_table()