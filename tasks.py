import os
import logging
import random

import celery
from celery import shared_task
from celery.worker.state import requests

logging.basicConfig(filename='celery_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if os.path.exists('celery_logs.log'):
    logger.info('-' * 110)

@shared_task(bind=True)
def task_process_notification_1(self):
    try:
        if not random.choice([0, 1]):
            # mimic random error
            raise Exception()

        requests.post('https://httpbin.org/delay/5')
    except Exception as e:
        logger.error('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 5})
def task_process_notification_2(self):
    if not random.choice([0, 1]):
        # mimic random error
        raise Exception()

    requests.post('https://httpbin.org/delay/5')


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 7})
def task_process_notification_3(self):
    try:
        raise Exception('ESTÁ OCORRENDO UMA EXCEÇÃO COM BACKOFF')
    except Exception as e:
        logger.error(f'OCORREU UM ERRO: {e}')
        raise self.retry(e)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=False,
             retry_kwargs={'max_retries': 7})
def task_process_notification_4(self):
    try:
        raise Exception('ESTÁ OCORRENDO UMA EXCEÇÃO COM BACKOFF 5')
    except Exception as e:
        logger.error(f'OCORREU UM ERRO: {e}')
        raise self.retry(e)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_jitter=True,
             retry_kwargs={'max_retries': 7})
def task_process_notification_5(self):
    try:
        raise Exception('ESTÁ OCORRENDO UMA EXCEÇÃO COM JITTER E BACKOFF')
    except Exception as e:
        logger.error(f'OCORREU UM ERRO: {e}')
        raise self.retry(e)


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_kwargs = {'max_retries': 7}
    retry_backoff = True


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification_6(self):
    try:
        raise Exception('ESTÁ OCORRENDO UMA EXCEÇÃO COM JITTER')
    except Exception as e:
        logger.error(f'OCORREU UM ERRO: {e}')
        raise self.retry(e)
