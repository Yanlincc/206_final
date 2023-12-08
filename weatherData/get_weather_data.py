
import requests

API_KEY = 'thILcTseiymmqagfHzmLMzOtFiEIvSlR'
ENDPOINT = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
HEADERS = {'token': API_KEY}

def fetch_avg_temperature(state_fips_code, year, start_month, end_month):
    temperatures = []
    for month in range(start_month, end_month + 1):
        params = {
            'datasetid': 'GHCND',
            'datatypeid': 'TAVG',
            'locationid': f'FIPS:{state_fips_code}',
            'startdate': f'{year}-{month:02d}-01',
            'enddate': f'{year}-{month:02d}-02',
            'units': 'standard',
            'limit': 1000,
        }
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        data = response.json()
        monthly_temps = [item['value'] for item in data['results']]
        avg_month_temp = sum(monthly_temps) / len(monthly_temps)
        temperatures.append(avg_month_temp)

    average_temperature = sum(temperatures) / len(temperatures)
    return average_temperature


def fetch_quarterly_avg_temperature(state_fips_code, year, quarter):
    if quarter == 1:
        return fetch_avg_temperature(state_fips_code, year, 1, 3)
    elif quarter == 2:
        return fetch_avg_temperature(state_fips_code, year, 4, 6)
    elif quarter == 3:
        return fetch_avg_temperature(state_fips_code, year, 7, 9)
    elif quarter == 4:
        return fetch_avg_temperature(state_fips_code, year, 10, 12)


def fetch_all_data():
    state_fips = {
        'al': '01', 'ak': '02', 'az': '04', 'ar': '05', 'ca': '06',
        'co': '08', 'ct': '09', 'de': '10', 'fl': '12', 'ga': '13',
        'hi': '15', 'id': '16', 'il': '17', 'in': '18', 'ia': '19',
        'ks': '20', 'ky': '21', 'la': '22', 'me': '23', 'md': '24',
        'ma': '25', 'mi': '26', 'mn': '27', 'ms': '28', 'mo': '29',
        'mt': '30', 'ne': '31', 'nv': '32', 'nh': '33', 'nj': '34',
        'nm': '35', 'ny': '36', 'nc': '37', 'nd': '38', 'oh': '39',
        'ok': '40', 'or': '41', 'pa': '42', 'ri': '44', 'sc': '45',
        'sd': '46', 'tn': '47', 'tx': '48', 'ut': '49', 'vt': '50',
        'va': '51', 'wa': '53', 'wv': '54', 'wi': '55', 'wy': '56'
    }
    for i in state_fips:
        fips = state_fips[i]
        print(fips)
        state_fips[i] = {}
        for j in range(1,5):
            try:
                state_fips[i][f'q{j}'] = fetch_quarterly_avg_temperature(fips, 2022, j)
            except:
                state_fips[i][f'q{j}'] = 0
                pass
    return state_fips



