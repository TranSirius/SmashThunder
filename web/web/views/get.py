from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web import databases

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

mod = Blueprint('get', __name__, url_prefix = '/get')

@mod.route('/upload/pic', methods = ['POST'])
def uploadPic():
    ret = dict()
    user_id = session.get['ID']
    if user_id == None:
        ret['status'] = 'please login first'
        return ret

    db_session = databases.db_session()
    query_res = db_session.query(databases.User).filter_by(ID = user_id).first()
    if query_res == None:
        ret['status'] = 'please login first'
        return ret
    
    user_name = query_res.user_name
    pic_dir = '/share/data/' + user_name + '/img/'

    request.files.get()

    ret['status'] = 'ok'
    return ret
    

@mod.route('/upload/md', methods = ['POST'])
def uploadMd():
    pass