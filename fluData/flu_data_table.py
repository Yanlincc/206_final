import sqlite3
from fluData.get_flu_data import get_flu_data
def create_flu_table():
    conn = sqlite3.connect('./database.db')

    cursor = conn.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS flu_data (
            state TEXT NOT NULL,
            quarter TEXT NOT NULL,
            WILI REAL,
            PRIMARY KEY (state, quarter)
        )
    '''

    cursor.execute(create_table_query)

    conn.commit()
    conn.close()

def insert_flu_data(state, q, wili):
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO flu_data (state, quarter, WILI)
        VALUES (?, ?, ?)
    ''', (state, q, wili,))
    conn.commit()
    conn.close()

def construct_flu_table():
    data = get_flu_data()
    create_flu_table()
    print(data)
    for i, j in data.items():
        for n, v in j.items():
            insert_flu_data(i, n, v)
