from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web.db import databases
from web.db.datamodels import User, Album, Photo

mod = Blueprint('get', __name__, url_prefix = '/get')

@mod.route('/album', methods = ['POST'])
def album():
    ret = dict()
    db_session = databases.db_session()
    user_name = request.json['username']
    request_user = db_session.query(User).filter(User.user_name == user_name).first()

    if request_user == None:
        ret['status'] = 'User Does Not Exist!'
        return ret
        
    request_user_id = request_user.ID
    target_album = None
    if 'target' in request.json:
        target_album = request.json['target']

    if target_album is None:
        album_list = db_session.query(Album).join(User).filter(User.ID == request_user_id).all()
    else:
        album_list = db_session.query(Album).join(User).filter(User.ID == request_user_id, Album.album_title == target_album).all()

    ret_album = []
    for album in album_list:
        album_title = album.album_title
        create_time = album.create_time
        photos = db_session.query(Photo).join(Album).join(User).filter(User.user_name == user_name).filter(Album.album_title == album_title)
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

    ret['albums'] = ret_album
    ret['status'] = 'ok'
    return ret


