import requests
import sqlite3

def create_cities_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            href TEXT,
            name TEXT,
            countryCode TEXT,
            latLng TEXT,
            population INTEGER
        )
    ''')
    connection.commit()

def save_cities_to_database(connection, cities_data, country_code):
    cursor = connection.cursor()

    for city_info in sorted(cities_data, key=lambda x: x.get("name", "")):
        cursor.execute('''
            INSERT INTO cities (href, name, countryCode, latLng, population)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            city_info.get("href", ""),
            city_info.get("name", ""),
            country_code,
            str(city_info.get("latLng", "")),
            city_info.get("population", 0),
        ))

    connection.commit()



def get_cities_by_country(country_code, limit=10):
    url = "https://geography4.p.rapidapi.com/apis/geography/v1/city"
    querystring = {"countryCode": country_code, "limit": str(limit)}
    headers = {
        "X-RapidAPI-Key": "4ea9633209msh981695f9bdbdfcep1c2032jsn541621e62793",
        "X-RapidAPI-Host": "geography4.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)


    cities_data = response.json()

        # Connect to SQLite database
    with sqlite3.connect('geography_data.db') as connection:
            # Create the cities table if it doesn't exist
        create_cities_table(connection)

            # Save the cities data into the database
        save_cities_to_database(connection, cities_data, country_code)

    return cities_data


# Example usage: Get cities in the US with a limit of 10 and save to the database
result = get_cities_by_country("US", limit=30)
if result:
    print(result)
