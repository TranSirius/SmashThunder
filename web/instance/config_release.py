DEBUG = False
USER_DATA = '/share/'
DATABASE_ENGINE = 'mysql+mysqldb://SmashThunder:awoehr23r3f2OFWE23092@localhost/SmashThunder?charset=utf8'
SECRET_KEY = 'AWUEHRAJFLAUWERLJANFDJAW'
HOST = '127.0.0.1'
PORT = 3000
ELASTIC_SEARCH_INDEX = {
    "USER": "user",
    "PHOTO": "photo",
    "POST": "post",
    "COMMENT": "comment"
}
PAGE_SIZE = 20