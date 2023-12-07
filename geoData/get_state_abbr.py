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
            '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA', '08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC',
            '12': 'FL', '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN', '19': 'IA', '20': 'KS', '21': 'KY',
            '22': 'LA', '23': 'ME', '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS', '29': 'MO', '30': 'MT',
            '31': 'NE', '32': 'NV', '33': 'NH', '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND', '39': 'OH',
            '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI', '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT',
            '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI', '56': 'WY', '00':'PR'
        }

        state_info = [(entry[0], fips_to_abbrev.get(entry[1], 'Unknown')) for entry in data[1:]]
        return state_info
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def create_database(data):
    conn = sqlite3.connect('./database.db')

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            state_name TEXT,
            state_abbrev TEXT
        )
    ''')

    cursor.executemany('INSERT INTO states VALUES (?, ?)', data)

    conn.commit()

    conn.close()

state_info = get_us_state_abbreviations()
if state_info:
    for state_name, state_abbrev in state_info:
        print(f"{state_name}, {state_abbrev}")

    create_database(state_info)
else:
    print("API call failed.")
