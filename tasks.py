import os
import logging
from datetime import datetime, timedelta
import backoff
from celery import shared_task

# Configuração do logger
logging.basicConfig(filename='celery_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Verifica se o arquivo de log já existe
if os.path.exists('celery_logs.log'):
    logger.info('-' * 80)


@shared_task(bind=True, acks_late=False, countdown=12)
@backoff.on_exception(backoff.expo, Exception, max_tries=10, jitter=backoff.full_jitter)
def generic_task(self):
    try:
        raise Exception("Ocorreu um erro")
    except Exception as e:
        time_retry = datetime.now() + timedelta(minutes=2)
        logger.info(f'Erro: {e}')
        self.retry(eta=time_retry)


# Executa a tarefa
generic_task()
