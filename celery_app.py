from celery import Celery

from settings import REFRESH_RATE_IN_MINUTES, MONGO_USER, MONGO_PASSWORD, MONGO_DB
from repositories import load_images, PictureStore

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(REFRESH_RATE_IN_MINUTES * 60.0, reload_cache.s(), name='Reload cache')

    
@app.task
def reload_cache():
    picture_store = PictureStore(user=MONGO_USER, password=MONGO_PASSWORD, db_name=MONGO_DB)
    load_images(picture_store)