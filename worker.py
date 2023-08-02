import os
import time

from celery import Celery
import requests

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
#cambiar a rabbitmq
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(url):
    proxies = {
        'http': 'socks5h://tor-socks-proxy:9150',
        'https': 'socks5h://tor-socks-proxy:9150'
    }

    response = requests.get(url, proxies=proxies)
    print(response.text)
    # escribir a redis
    
    return True