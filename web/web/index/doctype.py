from datetime import datetime
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text

from web.index.esclient import es

class User(Document):
    user_name = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )

class Photo(Document):
    album_id = Keyword()
    album_name = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )
    photo_name = Text(
        analyzer = "ik_max_word",
        search_analyzer = "ik_max_word"
    )