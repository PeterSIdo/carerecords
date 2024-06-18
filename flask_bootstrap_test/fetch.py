import sqlite3

# Path to the database
db_path = r'C:\Users\Peter\Documents\Care-Home-4\care4.db'

def fetch_first_names(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a query to fetch first names from the residents table
    cursor.execute('SELECT first_name FROM residents')
    first_names = cursor.fetchall()

    # Close the connection
    conn.close()

    # Print the fetched first names
    for name in first_names:
        print(name[0])

if __name__ == "__main__":
    fetch_first_names(db_path)