from fluData.flu_data_table import *
from geoData.merge import merge_tables
from weatherData.weather_table import construct_weather_table
def construct_db():
    construct_flu_table()
    create_flu_table()
    merge_tables()
    construct_weather_table()

if __name__ == '__main__':
    construct_db()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
