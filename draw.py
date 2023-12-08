import sqlite3
import matplotlib.pyplot as plt
import numpy as np

# 连接到数据库
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 获取 flu_data 表中的数据
cursor.execute('SELECT state, WILI FROM flu_data')
flu_data = dict(cursor.fetchall())

# 获取 merged_data 表中的数据
cursor.execute('SELECT state_abbrev, population FROM merged_data')
merged_data = dict(cursor.fetchall())

# 关闭数据库连接
conn.close()

# 提取共有的州的数据
common_states = set(flu_data.keys()) & set(merged_data.keys())

# 提取数据
states = list(common_states)
population_values = [merged_data[state_abbrev] for state_abbrev in states]
wili_values = [flu_data[state] for state in states]

# 创建柱状图
bar_width = 0.35
index = np.arange(len(states))

fig, ax = plt.subplots()
bar1 = ax.bar(index, population_values, bar_width, label='Population')
bar2 = ax.bar(index + bar_width, wili_values, bar_width, label='WILI')

# 设置图表标签等
ax.set_xlabel('States')
ax.set_ylabel('Values')
ax.set_title('Population and WILI by State')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(states)
ax.legend()

# 显示柱状图
plt.show()
