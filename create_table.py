import sqlite3

def create_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # SQL command to create table
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS care_frequency (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_initials TEXT,
        timestamp DATETIME,
        mattress_appropriate TEXT,
        cushion_appropriate TEXT,
        functionality_check TEXT,
        pressure_areas_checked TEXT,
        redness_present TEXT,
        keep_moving TEXT,
        incontinence_urine TEXT,
        incontinence_bowels TEXT,
        diet_intake TEXT,
        fluid_intake TEXT,
        supplement_intake TEXT,
        staff_initials TEXT
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