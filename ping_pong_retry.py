import logging
from datetime import datetime, timedelta
import backoff
import matplotlib.pyplot as plt
import pandas as pd
import random

# Configuração do logger
logging.basicConfig(filename='celery_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Função para simular uma chamada com jitter
@backoff.on_exception(backoff.expo, Exception, max_tries=5, jitter=backoff.full_jitter)
def make_call():
    # Simula uma chamada
    if random.random() < 0.8:
        raise Exception("Ocorreu um erro")
    else:
        return "Chamada bem-sucedida"


# Lista para armazenar os timestamps das chamadas
timestamps = []

# Realiza chamadas com jitter e registra os timestamps
for _ in range(10):
    try:
        result = make_call()
        logger.info(f'Chamada bem-sucedida: {result}')
    except Exception as e:
        time_retry = datetime.now() + timedelta(minutes=2)
        logger.info(f'Erro: {e}')
        continue
    timestamps.append(datetime.now())

# Gera o gráfico
hourly_counts = {}
for timestamp in timestamps:
    hour = timestamp.replace(minute=0, second=0)
    if hour in hourly_counts:
        hourly_counts[hour] += 1
    else:
        hourly_counts[hour] = 1

hours = list(hourly_counts.keys())
counts = list(hourly_counts.values())

plt.figure(figsize=(10, 6))
plt.plot(hours, counts)
plt.xlabel('Hora')
plt.ylabel('Número de Chamadas Bem-Sucedidas')
plt.title('Número de Chamadas Bem-Sucedidas ao Longo do Tempo')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
