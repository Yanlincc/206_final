import sqlite3
from .get_state_abbr import get_us_state_abbreviations
from .get_state_population import construct_population_table

def merge_tables():
    conn = sqlite3.connect('../database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS merged_data (
            id INTEGER PRIMARY KEY,
            state_name TEXT,
            state_abbrev TEXT,
            population INTEGER
        )
    ''')

    cursor.execute('SELECT * FROM population')
    population_data = cursor.fetchall()

    cursor.execute('SELECT * FROM states')
    state_abbrev_data = cursor.fetchall()

    for population_entry in population_data:
        state_name = population_entry[1]
        population = population_entry[2]

        state_abbrev = next((entry[2] for entry in state_abbrev_data if entry[1] == state_name), 'Unknown')

        cursor.execute('''
            INSERT OR REPLACE INTO merged_data (state_name, state_abbrev, population)
            VALUES (?, ?, ?)
        ''', (state_name, state_abbrev, population))

    conn.commit()
    conn.close()

def construct_tables():
    get_us_state_abbreviations()
    construct_population_table()
    merge_tables()
