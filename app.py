from flask import Flask

from usecases import search_for_pictures
from repositories import PictureStore, load_images
from schemas import Picture
from settings import MONGO_USER, MONGO_PASSWORD, MONGO_DB


app = Flask(__name__)
picture_schema = Picture()
picture_store = PictureStore(user=MONGO_USER, password=MONGO_PASSWORD, db_name=MONGO_DB)
load_images(picture_store)


@app.route('/search/<search_term>')
def search_images(search_term):
    pictures = search_for_pictures(search_term, picture_store)
    return {"pictures": picture_schema.dump(pictures, many=True)}, 200