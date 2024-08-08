import sqlite3

def fix_residents_table():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    
    # Step 1: Create a temporary table and copy data
    cursor.execute('''
        CREATE TEMPORARY TABLE temp_residents AS
        SELECT resident_name, resident_surname, unit_name, room_nr, resident_initials FROM residents
    ''')
    
    # Step 2: Drop the original table
    cursor.execute('DROP TABLE residents')
    
    # Step 3: Recreate the table with the correct schema
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS residents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_name TEXT,
        resident_surname TEXT,
        unit_name TEXT,
        room_nr INTEGER,
        resident_initials TEXT
    )
    '''
    cursor.execute(create_table_sql)
    
    # Step 4: Re-insert data from the temporary table
    cursor.execute('''
        INSERT INTO residents (resident_name, resident_surname, unit_name, room_nr, resident_initials)
        SELECT resident_name, resident_surname, unit_name, room_nr, resident_initials FROM temp_residents
    ''')
    
    # Commit changes
    conn.commit()
    
    # Step 5: Drop the temporary table
    cursor.execute('DROP TABLE temp_residents')
    
    # Close the connection
    conn.close()
    
    print('Residents table has been fixed successfully!', 'success')

# Call the function
fix_residents_table()