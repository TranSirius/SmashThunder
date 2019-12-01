from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text

from web.index.esclient import es
from flask import current_app as app

class User(Document):
    user_name = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )

    class Index:
        name = app.config['ELASTIC_SEARCH_INDEX']['USER']
        settings = {
            "number_of_shards": 0,
        }

class Photo(Document):
    photo_name = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )

    class Index:
        name = app.config['ELASTIC_SEARCH_INDEX']['PHOTO']
        settings = {
            "number_of_shards": 0,
        }

class Post(Document):
    post_title = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )
    post_content = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )
    folder_name = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )

    class Index:
        name = app.config['ELASTIC_SEARCH_INDEX']['POST']
        settings = {
            "number_of_shards": 0,
        }

class Comment(Document):
    content = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )

    class Index:
        name = app.config['ELASTIC_SEARCH_INDEX']['COMMENT']
        settings = {
            "number_of_shards": 0,
        }