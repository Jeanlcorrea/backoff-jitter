import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('backoff_results.csv')

grouped_data = data.groupby('Algorithm')

for name, group in grouped_data:
    plt.plot(group['clients'], group['calls'], label=name)

plt.xlabel('Número de Clientes')
plt.ylabel('Número de Chamadas')
plt.title('Número de Chamadas em Função do Número de Clientes para Cada Algoritmo de Backoff')
plt.legend()

plt.show()
