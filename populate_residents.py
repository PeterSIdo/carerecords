import csv
import sqlite3
import os

def clear_residents_table(db_path):
    try:
        print(f"Attempting to connect to the database at {db_path}...")
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        print("Connected to the database.")
        
        cursor.execute('DELETE FROM residents')
        conn.commit()
        conn.close()
        print('All residents deleted successfully.')
    except Exception as e:
        print(f"An error occurred while clearing the residents table: {e}")

def import_residents_from_csv(db_path, csv_path):
    try:
        print("Clearing the residents table...")
        clear_residents_table(db_path)  # Clear the table before importing new data
        
        print(f"Connecting to the database at {db_path}...")
        conn = sqlite3.connect(db_path, timeout=10)
        cursor = conn.cursor()
        print('Connected to the database.')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS residents (
                            id INTEGER PRIMARY KEY, 
                            first_name TEXT, 
                            surname TEXT, 
                            unit_name TEXT, 
                            room_nr INTEGER,
                            resident_initials TEXT)''')
        print('Table created or already exists.')

        expected_headers = ['first_name', 'surname', 'unit_name', 'room_nr']

        print(f"Opening CSV file at {csv_path}...")
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            print(f"CSV headers: {headers}")
            
            if headers != expected_headers:
                print(f"CSV header mismatch. Expected headers: {expected_headers}, but got: {headers}")
                return
            
            for row in reader:
                first_name = row.get('first_name', '').strip()
                surname = row.get('surname', '').strip()
                unit_name = row.get('unit_name', '').strip()
                room_nr = row.get('room_nr', '').strip()

                if not room_nr.isdigit():
                    print(f"Invalid room number: {room_nr}")
                    continue

                room_nr = int(room_nr)

                if first_name and surname:
                    initials = first_name[0].upper() + surname[0].upper()
                    resident_initials = f"{room_nr:02d}{initials}{int(unit_name):02d}"

                    cursor.execute('''
                        INSERT INTO residents (first_name, surname, unit_name, room_nr, resident_initials)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (first_name, surname, unit_name, room_nr, resident_initials))
                    print(f'Inserted: {first_name} {surname} into residents table.')

        conn.commit()
        conn.close()
        print('Residents imported successfully.')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    db_path = r'C:\Users\Peter\Documents\Care-Home-4\care4.db'
    csv_path = r'C:\Users\Peter\Documents\Care-Home-4\residents-tab-csv.csv'
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
    elif not os.path.exists(csv_path):
        print(f"CSV file not found at {csv_path}")
    else:
        import_residents_from_csv(db_path, csv_path)