import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password"
)

# Create a cursor object
cur = conn.cursor()

# Define the SQL query with parameter placeholders
query = "INSERT INTO your_table (name, age, city) VALUES (%s, %s, %s)"

# Define the parameter values as a tuple
values = ("John Smith", 30, "New York")

# Execute the query with the parameter values
cur.execute(query,values)

# Commit the transaction
conn.commit()

# Close the cursor and database connection
cur.close()
conn.close()