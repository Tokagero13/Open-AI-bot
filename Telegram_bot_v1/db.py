import psycopg2
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Define your connection parameters
dbname = DB_NAME
user = DB_NAME
password = DB_PASS
host = DB_HOST  # Typically "localhost" if the database is on your local machine
port = DB_PORT  # Typically 5432 for PostgreSQL

# Establish a connection to the database
def db_connect():
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connected to the database!")
        
        # Create a cursor object to execute SQL queries
        # cursor = connection.cursor()

        # Execute SQL queries using the cursor
        # cursor.execute("SELECT * FROM your_table")
        
        # Fetch all rows from the result set
        # rows = cursor.fetchall()
        
        # Iterate over the rows and print them
        # for row in rows:
        #     # Decode each element of the row using the specified encoding
        #     decoded_row = [element.decode('utf-8') for element in row]
        #     print(decoded_row)

        # Close the cursor and connection
        # cursor.close()
        # connection.close()
        # print("Connection closed.")
        
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)

def main():
    db_connect()

if __name__ == "__main__":
    main()