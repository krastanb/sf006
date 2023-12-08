from celery import shared_task
import time

@shared_task
def hello():
    for i in range(10):
        time.sleep(1)
        print(i)
