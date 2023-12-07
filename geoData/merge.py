import sqlite3

def merge_tables():
    # Connect to the existing database
    conn = sqlite3.connect('../database.db')
    cursor = conn.cursor()

    # Create the merged_data table in the existing database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS merged_data (
            id INTEGER PRIMARY KEY,
            state_name TEXT,
            state_abbrev TEXT,
            population INTEGER
        )
    ''')

    # Fetch data from the population table
    cursor.execute('SELECT * FROM population')
    population_data = cursor.fetchall()

    # Fetch data from the states table
    cursor.execute('SELECT * FROM states')
    state_abbrev_data = cursor.fetchall()

    # Merge data based on state_name
    for population_entry in population_data:
        state_name = population_entry[1]  # Assuming state_name is the second column, modify accordingly
        population = population_entry[2]   # Assuming population is the third column, modify accordingly

        # Find the corresponding state_abbrev from state_abbrev_data
        state_abbrev = next((entry[2] for entry in state_abbrev_data if entry[1] == state_name), 'Unknown')

        # Insert into the merged_data table
        cursor.execute('''
            INSERT OR REPLACE INTO merged_data (state_name, state_abbrev, population)
            VALUES (?, ?, ?)
        ''', (state_name, state_abbrev, population))

    # Commit and close connection
    conn.commit()
    conn.close()

# Call the function to merge tables
merge_tables()
