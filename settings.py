import os

REFRESH_RATE_IN_MINUTES = int(os.getenv('CACHE_REFRESH_RATE', '1'))
API_KEY = os.getenv('API_KEY', '23567b218376f79d9415')

MONGO_USER = 'user'
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_DB = 'pictures'