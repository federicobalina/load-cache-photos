import requests
from functools import wraps

import pymongo

from settings import API_KEY, MONGO_USER, MONGO_PASSWORD, MONGO_DB

API_URL = 'http://interview.agileengine.com/{}'
API_AUTH_ENDPOINT = API_URL.format('auth')
API_IMAGES_ENDPOINT = API_URL.format('images')
API_IMAGE_DETAIL_ENDPOINT = API_URL.format('images/{}')

TOKEN_BEARER = 'Bearer {}'

ACCESS_TOKEN = None


class APIUnauthorized(Exception):
	pass


def retry(max_retries, exception, remediation):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			attempt = 1
			while attempt < max_retries:
				try:
					return func(*args, **kwargs)
				except exception:
					remediation()
					attempt += 1
			return func(*args, **kwargs)
		return wrapper
	return decorator


def get_access_token():
	response = requests.post(API_AUTH_ENDPOINT, json={
		'apiKey': API_KEY
	})
	if response.status_code == 200:
		body = response.json()
		return body['token']


def renew_token():
	global ACCESS_TOKEN
	new_token = None
	while new_token is None:
		new_token = get_access_token()
	ACCESS_TOKEN = new_token


@retry(2, APIUnauthorized, renew_token)
def load_images_page(page_number, store):
	headers = {'Authorization': TOKEN_BEARER.format(ACCESS_TOKEN)}
	query_params = {'page': page_number}
	response = requests.get(API_IMAGES_ENDPOINT, params=query_params, headers=headers)
	if response.status_code == 401:
		raise APIUnauthorized
	body = response.json()
	pictures = body['pictures']
	for picture in pictures:
		details = load_image_details(picture['id'])
		store.add_picture(details)
	return body['hasMore']


def load_images(store):
	current_page = 1
	more_pages = True

	while more_pages:
		more_pages = load_images_page(current_page, store)
		current_page += 1


@retry(2, APIUnauthorized, renew_token)
def load_image_details(image_id):
	headers = {'Authorization': TOKEN_BEARER.format(ACCESS_TOKEN)}
	response = requests.get(API_IMAGE_DETAIL_ENDPOINT.format(image_id), headers=headers)
	if response.status_code == 401:
		raise APIUnauthorized
	return response.json()


class PictureStore:
	def __init__(self, user, password, db_name):
		self.client = pymongo.MongoClient('mongodb+srv://{}:{}@cluster0.opbyq.mongodb.net/{}?retryWrites=true&w=majority'.format(
			user, password, db_name))
		self.db = self.client.test
		self.pictures = self.db.pictures

	def add_picture(self, picture_json):
		self.pictures.replace_one({'id': picture_json['id']}, picture_json, upsert=True)

	def get_all_pictures(self):
		return self.pictures.find()
