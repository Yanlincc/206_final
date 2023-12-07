import sqlite3
import requests

def create_database():
    # 连接到 SQLite 数据库（如果不存在，则会创建）
    connection = sqlite3.connect("population_data.db")

    # 创建一个游标对象，用于执行 SQL 语句
    cursor = connection.cursor()

    # 创建一个表格用于存储人口数据
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS population (
            state_name TEXT PRIMARY KEY,
            population INTEGER
        )
    ''')

    # 提交并关闭连接
    connection.commit()
    connection.close()

def insert_population_data():
    # 连接到 SQLite 数据库
    connection = sqlite3.connect("population_data.db")
    cursor = connection.cursor()

    # 获取人口数据
    base_url = "https://api.census.gov/data/2020/acs/acs5"
    query_params = {
        "get": "NAME,B01003_001E",
        "for": "state:*",
    }
    url = f"{base_url}?{('&'.join(f'{key}={value}' for key, value in query_params.items()))}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # 将人口数据插入到数据库中
        for entry in data[1:]:
            state_name = entry[0]
            population = entry[1]
            cursor.execute('''
                INSERT OR REPLACE INTO population (state_name, population)
                VALUES (?, ?)
            ''', (state_name, population))

        # 提交并关闭连接
        connection.commit()
        connection.close()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        connection.close()

# 创建数据库和表格
create_database()

# 插入人口数据到数据库
insert_population_data()
