import sqlite3
import matplotlib.pyplot as plt

def plot_flu_cases_vs_population(database_path='database.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = """
        SELECT merged_data.state_abbrev, 
               AVG(flu_data.num_patients) AS avg_flu_cases,
               merged_data.population
        FROM flu_data
        INNER JOIN merged_data ON flu_data.state = merged_data.state_abbrev
        GROUP BY merged_data.state_abbrev;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    state_abbrevs = []
    avg_flu_cases = []
    populations = []

    for result in results:
        state_abbrevs.append(result[0])
        avg_flu_cases.append(result[1])
        populations.append(result[2])

    conn.close()

    fig, ax1 = plt.subplots(figsize=(12, 8))

    ax1.bar(state_abbrevs, avg_flu_cases, color='skyblue', label='Average Flu Cases')

    ax1.set_ylabel('Average Flu Cases')
    ax1.set_xlabel('State Abbrev')
    ax1.set_title('Average Flu Cases by State')

    ax2 = ax1.twinx()
    ax2.plot(state_abbrevs, populations, color='red', marker='o', label='Population')
    ax2.set_ylabel('Population')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.show()

