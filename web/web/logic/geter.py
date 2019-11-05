from web.db.datamodels import *
from web.db.databases import db_session

class GetPhotos():
    def __call__(self, user_name, album_name = None):
        db_session_instance = db_session()
        if album_name is None:
            album_list = db_session_instance.query(Album).join(User).filter(User.user_name == user_name).all()
        else:
            album_list = db_session_instance.query(Album).join(User).filter(User.user_name == user_name, Album.album_title == album_name).all()

        user_name = db_session_instance.query(User).filter(User.user_name == user_name).first().user_name
        ret_album = []
        for album in album_list:
            album_title = album.album_title
            create_time = album.create_time
            photos = db_session_instance.query(Photo).join(Album).join(User).filter(User.user_name == user_name).filter(Album.album_title == album_title)
            photo_list = []
            for photo in photos:
                single_photo = dict()
                single_photo['url'] = '/data/' + user_name + '/img/' + album_title + '/' + photo.photo_title
                single_photo['title'] = photo.photo_title
                single_photo['time'] = photo.create_time
                photo_list.append(single_photo)
            single_album = dict()
            single_album['title'] = album_title
            single_album['createTime'] = create_time
            single_album['imgs'] = photo_list
            ret_album.append(single_album)
        return ret_album

class GetPosts():
    pass