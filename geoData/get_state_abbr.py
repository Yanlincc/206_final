import sqlite3
import requests


def get_us_state_abbreviations():
    base_url = "https://api.census.gov/data/2020/acs/acs5"

    query_params = {
        "get": "NAME,STATE",
        "for": "state:*",
    }

    url = f"{base_url}?{('&'.join(f'{key}={value}' for key, value in query_params.items()))}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        fips_to_abbrev = {
            '01': 'al', '02': 'ak', '04': 'az', '05': 'ar', '06': 'ca', '08': 'co', '09': 'ct', '10': 'de', '11': 'dc',
            '12': 'fl', '13': 'ga', '15': 'hi', '16': 'id', '17': 'il', '18': 'in', '19': 'ia', '20': 'ks', '21': 'ky',
            '22': 'la', '23': 'me', '24': 'md', '25': 'ma', '26': 'mi', '27': 'mn', '28': 'ms', '29': 'mo', '30': 'mt',
            '31': 'ne', '32': 'nv', '33': 'nh', '34': 'nj', '35': 'nm', '36': 'ny', '37': 'nc', '38': 'nd', '39': 'oh',
            '40': 'ok', '41': 'or', '42': 'pa', '44': 'ri', '45': 'sc', '46': 'sd', '47': 'tn', '48': 'tx', '49': 'ut',
            '50': 'vt', '51': 'va', '53': 'wa', '54': 'wv', '55': 'wi', '56': 'wy', '72': 'pr'
        }

        state_info = [(entry[0], fips_to_abbrev.get(entry[1], 'Unknown')) for entry in data[1:]]
        return state_info
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def create_database(data):
    conn = sqlite3.connect('../database.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER,
            state_name TEXT,
            state_abbrev TEXT,
            PRIMARY KEY(id, state_name, state_abbrev)
        )
    ''')

    sorted_state_info = list(enumerate(sorted(data, key=lambda x: x[1])))

    try:cursor.executemany('INSERT INTO states VALUES (?, ?, ?)', [(item[0] + 1,) + item[1] for item in sorted_state_info])
    except: pass
    conn.commit()

    conn.close()


state_info = get_us_state_abbreviations()
if state_info:
    print("Original State Abbreviations:")
    for state_name, state_abbrev in state_info:
        print(f"{state_name}, {state_abbrev}")

    create_database(state_info)
else:
    print("API call failed.")
