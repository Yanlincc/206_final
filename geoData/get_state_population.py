import sqlite3
import requests

def create_database():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS population (
            id INTEGER PRIMARY KEY,
            state_name TEXT,
            population INTEGER
        )
    ''')

    connection.commit()
    connection.close()

def insert_population_data():
    connection = sqlite3.connect("./database.db")
    cursor = connection.cursor()

    base_url = "https://api.census.gov/data/2020/acs/acs5"
    query_params = {
        "get": "NAME,B01003_001E",
        "for": "state:*",
    }
    url = f"{base_url}?{('&'.join(f'{key}={value}' for key, value in query_params.items()))}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        sorted_data = sorted(data[1:], key=lambda x: x[0])

        for idx, entry in enumerate(sorted_data, start=1):
            state_name = entry[0]
            population = entry[1]
            cursor.execute('''
                INSERT OR REPLACE INTO population (id, state_name, population)
                VALUES (?, ?, ?)
            ''', (idx, state_name, population))

        connection.commit()
        connection.close()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        connection.close()

def construct_population_table():
    create_database()
    insert_population_data()
