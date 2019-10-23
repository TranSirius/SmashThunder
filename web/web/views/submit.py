from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

from web.db import databases
from web.db import datamodels
from web.db.datamodels import User, Album, Photo

from web.views.auth import loginRequest

import os

mod = Blueprint('submit', __name__, url_prefix = '/submit')

@mod.route('/img', methods = ['POST'])
@loginRequest
def uploadPic():
    ret = dict()

    db_session = databases.db_session()
    query_res = db_session.query(User).filter(User.ID == g.user_id).first()
    
    user_name = query_res.user_name
    pic_dir = app.config['USER_DATA'] + user_name + '/img/'

    img_list = request.files.getlist('files')
    time = request.form.get('time')
    album_title = request.form.get('albumTitle')

    album = db_session.query(Album).filter(Album.user_ID == g.user_id).filter(Album.album_title == album_title).first()
    if album is None:
        Album.generateAlbum(user_name, album_title)
        album = db_session.query(Album).filter(Album.user_ID == g.user_id).filter(Album.album_title == album_title).first()

    for img in img_list:
        img.save(app.config['USER_DATA'] + user_name + '/img/' + album_title + '/' + img.filename)
        new_img = Photo(album_ID = album.ID, photo_title = img.filename, create_time = time)
        db_session.add(new_img)

    ret['status'] = 'ok'
    db_session.commit()
    return ret
    

@mod.route('/md', methods = ['POST'])
def uploadMd():
    pass