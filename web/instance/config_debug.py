DEBUG = True
USER_DATA = '/share/'
DATABASE_ENGINE = 'mysql+mysqldb://test:test@localhost/test?charset=utf8'
SECRET_KEY = 'AWUEHRAIWE'
HOST = '127.0.0.1'
PORT = 3000
ELASTIC_SEARCH_INDEX = {
    "USER": "testuser",
    "PHOTO": "testphoto",
    "POST": "testpost",
    "COMMENT": "testcomment"
}
PAGE_SIZE = 20