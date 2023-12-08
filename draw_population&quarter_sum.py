import sqlite3
import matplotlib.pyplot as plt

def plot_flu_cases_by_quarter(database_path='database.db'):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = """
        SELECT merged_data.state_abbrev, 
               SUM(CASE WHEN flu_data.quarter = 'Q1' THEN flu_data.num_patients ELSE 0 END) AS Q1_total,
               SUM(CASE WHEN flu_data.quarter = 'Q2' THEN flu_data.num_patients ELSE 0 END) AS Q2_total,
               SUM(CASE WHEN flu_data.quarter = 'Q3' THEN flu_data.num_patients ELSE 0 END) AS Q3_total,
               SUM(CASE WHEN flu_data.quarter = 'Q4' THEN flu_data.num_patients ELSE 0 END) AS Q4_total,
               merged_data.population
        FROM flu_data
        INNER JOIN merged_data ON flu_data.state = merged_data.state_abbrev
        GROUP BY merged_data.state_abbrev;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    state_abbrevs = []
    Q1_totals = []
    Q2_totals = []
    Q3_totals = []
    Q4_totals = []
    populations = []

    for result in results:
        state_abbrevs.append(result[0])
        Q1_totals.append(result[1])
        Q2_totals.append(result[2])
        Q3_totals.append(result[3])
        Q4_totals.append(result[4])
        populations.append(result[5])

    conn.close()

    fig, ax1 = plt.subplots(figsize=(12, 8))

    ax1.bar(state_abbrevs, Q1_totals, label='Q1', alpha=0.8)
    ax1.bar(state_abbrevs, Q2_totals, bottom=Q1_totals, label='Q2', alpha=0.8)
    ax1.bar(state_abbrevs, Q3_totals, bottom=[i + j for i, j in zip(Q1_totals, Q2_totals)], label='Q3', alpha=0.8)
    ax1.bar(state_abbrevs, Q4_totals, bottom=[i + j + k for i, j, k in zip(Q1_totals, Q2_totals, Q3_totals)], label='Q4', alpha=0.8)

    ax1.set_ylabel('Flu Cases')
    ax1.set_xlabel('State Abbrev')
    ax1.set_title('Flu Cases by State and Quarter')

    ax2 = ax1.twinx()
    ax2.plot(state_abbrevs, populations, color='red', marker='o', label='Population')
    ax2.set_ylabel('Population')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.show()


