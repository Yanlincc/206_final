import requests
from statistics import mean

def get_flu_data():
    url = "https://api.delphi.cmu.edu/epidata/fluview/"

    flu_data = {}
    lst_states = ['nat', 'ca']
    lst_epiweeks = [range(202201, 202253)]
    for i in lst_states:
        params = {
            'regions': i,
            'epiweeks': lst_epiweeks,
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
        else:
            print("Failed to retrieve data: Status code", response.status_code)
            return
        flu_data[i] = {}
        flu_data[i]['Q1'] = round(mean([week_data['wili'] for week_data in data['epidata'][:13]]), 4)
        flu_data[i]['Q2'] = round(mean([week_data['wili'] for week_data in data['epidata'][14:26]]), 4)
        flu_data[i]['Q3'] = round(mean([week_data['wili'] for week_data in data['epidata'][27:39]]), 4)
        flu_data[i]['Q4'] = round(mean([week_data['wili'] for week_data in data['epidata'][40:]]), 4)
    return flu_data

get_flu_data()