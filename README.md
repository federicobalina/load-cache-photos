# load-cache-photos

## Create a virtual environment

python -m venv env

## Activate Virtual environment

Execute the activate script inside env/Scripts
./env/Scripts/activate

## Install requirements

pip install -r requirements.txt

## Set environment variables

The route to the flask application:
FLASK_APP=app.py

The interval in minutes that you want to refresh the cache:
CACHE_REFRESH_RATE

The API key to authenticate with it:
API_KEY

The password for the mongoDB user:
MONGO_PASSWORD

## Start flask application

python -m flask run

## Start celery beat process

celery beat -A celery_app