import sqlite3

def add_staff_initials_column():
    # Connect to the SQLite database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    
    # SQL command to add the new column
    add_column_sql = '''
    ALTER TABLE fluid_chart
    ADD COLUMN staff_initials TEXT
    '''
    
    # Execute the SQL command
    cursor.execute(add_column_sql)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to add the new column
add_staff_initials_column()