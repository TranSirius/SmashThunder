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
from web.db.datamodels import User, Follow

from web.index import doctype

from web.views.auth import loginRequest

mod = Blueprint('follow', __name__, url_prefix = '/follow')

@mod.route('', methods = ['POST'])
@loginRequest
def followAPI():
    ret = dict()
    db_session_instance = databases.db_session()
    try:
        follow_flag = request.json['follow']
        follow_target = request.json['target']
    except:
        ret['status'] = 'Request Format Error!'
        return ret

    followee_id = db_session_instance\
        .query(User)\
        .filter(User.user_name == follow_target)\
        .first()\
        .ID
    follower_id = g.user_id
    if followee_id == follower_id:
        ret['status'] = 'You Cannot Follow Yourself!'
        return ret

    if follow_target:
        follow = Follow(follower_id = follower_id, followee_id = followee_id)
        db_session_instance.merge(follow)
        db_session_instance.commit()
        ret['status'] = 'ok'
        return ret
    else:
        follow = db_session_instance\
            .query(Follow)\
            .filter(Follow.followee_id == followee_id).filter(Follow.follower_id == follower_id)\
            .delete()
        ret['status'] = 'ok'
        return ret

