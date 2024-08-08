import sqlite3

def drop_columns():
    # Connect to the SQLite database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # List of columns to be dropped
    columns_to_drop = ['resident_antibiotic']

    # Get the current table schema
    cursor.execute("PRAGMA table_info(residents)")
    columns_info = cursor.fetchall()

    # Extract column names excluding the ones to be dropped
    existing_columns = [col[1] for col in columns_info if col[1] not in columns_to_drop]

    # Create a temporary table with the remaining columns
    cursor.execute(f"""
        CREATE TABLE residents_temp AS
        SELECT {', '.join(existing_columns)}
        FROM residents
    """)

    # Drop the original table
    cursor.execute("DROP TABLE residents")

    # Rename the temporary table to the original table name
    cursor.execute("ALTER TABLE residents_temp RENAME TO residents")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    drop_columns()
    print("Columns dropped successfully.")