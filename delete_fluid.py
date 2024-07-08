import sqlite3

def delete_all_data_from_fluid_chart(db_path):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute the SQL command to delete all data from the fluid_chart table
        cursor.execute('DELETE FROM fluid_chart')
        
        # Commit the changes
        conn.commit()
        
        print("All data from the fluid_chart table has been deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = 'care4.db'  # Path to your SQLite database
    delete_all_data_from_fluid_chart(db_path)