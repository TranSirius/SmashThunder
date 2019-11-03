from flask import Blueprint
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web.db import databases
from web.db.datamodels import User, Album, Photo
from web.logic.geter import GetPhotos

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
    request_user_name = request_user.user_name
    target_album = None
    if 'target' in request.json:
        target_album = request.json['target']

    geter = GetPhotos()
    try:
        ret_album = geter(user_name = request_user_name, album_name = target_album)
        ret['albums'] = ret_album
    except:
        ret['status'] = "Something wrong"
    else:
        ret['status'] = 'ok'
        return ret


