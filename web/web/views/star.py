from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request
from flask import current_app as app

import sqlalchemy

from web.db import databases
from web.db import datamodels
from web.db.datamodels import User, Star, Folder, Post

from web.index import doctype

from web.views.auth import loginRequest

mod = Blueprint('star', __name__, url_prefix = '/star')

@mod.route('', methods = ['POST'])
@loginRequest
def submitStar():
    ret = dict()
    db_session_instance = databases.db_session()

    try:
        user = request.json['username']
        folder = request.json['folder']
        title = request.json['title']
        star_flag = request.json['star']
    except:
        ret['status'] = "Request Format Error!"
        return ret

    post = db_session_instance\
        .query(Post).join(Folder).join(User)\
        .filter(User.user_name == user).filter(Folder.folder_title == folder).filter(Post.post_title == title)\
        .first()

    if star_flag:
        star = Star(user_id = g.user_id, post_id = post.ID)
        db_session_instance.merge(star)
        db_session_instance.commit()
        ret['status'] = 'ok'
    else:
        db_session_instance\
            .query(Star)\
            .filter(Star.user_id == g.user_id).filter(Star.post_id == post.ID)
        db_session_instance.commit()
        ret['status'] = 'ok'
    return ret