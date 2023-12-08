import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from draw_population_quarter_avg import plot_flu_cases_vs_population
from draw_population_quarter_sum import plot_flu_cases_by_quarter


def draw_flu_and_population_bar():
    plot_flu_cases_vs_population()
    plot_flu_cases_by_quarter()

def draw_temp_flu_scatter():

    conn = sqlite3.connect('database.db')

    query = """
    SELECT f.state, f.quarter, f.num_patients,
           CASE f.quarter
               WHEN 'Q1' THEN t.q1_temp
               WHEN 'Q2' THEN t.q2_temp
               WHEN 'Q3' THEN t.q3_temp
               WHEN 'Q4' THEN t.q4_temp
           END AS temperature
    FROM flu_data f
    JOIN quarterly_temp t ON f.state = t.state_abbr
    """

    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    temperatures = [row[3] for row in data if row[3] is not None]
    num_patients = [row[2] for row in data if row[3] is not None]

    slope, intercept = np.polyfit(temperatures, num_patients, 1)
    line = np.poly1d((slope, intercept))

    temperatures = [row[3] for row in data]
    num_patients = [row[2] for row in data]

    plt.scatter(temperatures, num_patients, label = 'Data Points')
    plt.plot(temperatures, line(temperatures), color = 'red', label = 'Regression Line')
    plt.xlabel('Temperature (°F)')
    plt.ylabel('Number of Flu Patients')
    plt.title('Correlation between Temperature and Number of Flu Patients')
    plt.legend()
    plt.show()

    conn.close()



def draw_quarterly_flu_bar():

    conn = sqlite3.connect('database.db')

    flu_data_query = "SELECT * FROM flu_data"
    flu_data = pd.read_sql_query(flu_data_query, conn)

    temp_data_query = "SELECT * FROM quarterly_temp"
    temp_data = pd.read_sql_query(temp_data_query, conn)

    conn.close()

    merged_data = pd.merge(flu_data, temp_data, left_on='state', right_on='state_abbr')

    merged_data = merged_data[merged_data[['q1_temp', 'q2_temp', 'q3_temp', 'q4_temp']].mean(axis=1) != 0]

    average_temp = merged_data[['q1_temp', 'q2_temp', 'q3_temp', 'q4_temp']].mean()
    average_flu_patients = merged_data.groupby('quarter')['num_patients'].mean()

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Quarter')
    ax1.set_ylabel('Average Temperature', color=color)
    bars = ax1.bar(average_temp.index, average_temp, color=color, label='Average Temperature')
    ax1.tick_params(axis='y', labelcolor=color)

    for bar, label in zip(bars, average_temp):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, height + 0.1, f'{label:.2f}', ha='center', va='bottom', color='black')

    ax2 = ax1.twinx()  
    color = 'yellow'  
    ax2.set_ylabel('Average Flu Patients', color=color)  
    line = ax2.plot(average_flu_patients.index, average_flu_patients, color=color, marker='o', label='Average Flu Patients')
    ax2.tick_params(axis='y', labelcolor=color)

    for i, txt in enumerate(average_flu_patients):
        ax2.annotate(f'{txt:.2f}', (average_flu_patients.index[i], txt + 10000), color='black', ha='center', va='bottom')

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left', bbox_to_anchor=(0.7, 1.0))

    plt.title('Comparison between Average Temperature and Average Flu Patient Number')
    plt.show()



if __name__ == '__main__':
    draw_flu_and_population_bar()
    draw_quarterly_flu_bar()
    draw_temp_flu_scatter()