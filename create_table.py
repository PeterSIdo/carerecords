import sqlite3

def create_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS report_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_name TEXT
    )
    '''

    # Execute the SQL command
    cursor.execute(create_table_sql)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Table created successfully.")