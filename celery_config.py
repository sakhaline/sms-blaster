import os
from datetime import timedelta
from dotenv import load_dotenv

from celery import Celery


load_dotenv()

CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "")
CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "")


app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


app.conf.beat_schedule = {
    'refresh-auth-token-every-12-hours': {
        'task': 'tasks.refresh_auth_token_task',
        'schedule': timedelta(seconds=5),
    },
}
