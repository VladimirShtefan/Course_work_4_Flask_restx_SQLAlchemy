import os

import psycopg2

# establishing the connection
conn = psycopg2.connect(
    database='postgres', user=os.getenv('POSTGRES_USERNAME'), password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST', '127.0.0.1'), port=os.getenv('POSTGRES_PORT', 5555)
)
conn.autocommit = True

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Preparing query to create a database
sql = '''CREATE database mydb'''

# Creating a database
cursor.execute(sql)
print("Database created successfully........")

# Closing the connection
conn.close()
