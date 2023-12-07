import sqlite3

def merge_tables():
    conn1 = sqlite3.connect('../database.db')
    cursor1 = conn1.cursor()


    cursor1.execute('''
        CREATE TABLE IF NOT EXISTS merged_data (
            state_name TEXT PRIMARY KEY,
            population INTEGER,
            state_abbrev TEXT
        )
    ''')

    cursor1.execute('SELECT * FROM population')
    population_data = cursor1.fetchall()

    cursor1.execute('SELECT * FROM states')
    state_abbrev_data = cursor1.fetchall()

    for population_entry in population_data:
        state_name = population_entry[0]
        population = population_entry[1]

        state_abbrev = next((entry[1] for entry in state_abbrev_data if entry[0] == state_name), 'Unknown')

        cursor1.execute('''
            INSERT OR REPLACE INTO merged_data (state_name, population, state_abbrev)
            VALUES (?, ?, ?)
        ''', (state_name, population, state_abbrev))

    conn1.commit()
    conn1.close()

merge_tables()
