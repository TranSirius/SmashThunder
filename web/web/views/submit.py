from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import request

from web import databases

mod = Blueprint('submit', __name__, url_prefix = '/submit')

@mod.route('/img', methods = ['POST'])
def uploadPic():
    ret = dict()
    # user_id = session.get('ID')
    # if user_id == None:
    #     ret['status'] = 'please login first'
    #     return ret

    # db_session = databases.db_session()
    # query_res = db_session.query(databases.User).filter_by(ID = user_id).first()
    # if query_res == None:
    #     ret['status'] = 'please login first'
    #     return ret
    
    # user_name = query_res.user_name
    # pic_dir = '/share/data/' + user_name + '/img/'

    img_list = request.files.getlist('files')
    for img in img_list:
        print(img.__dict__)
        img.save('/share/' + img.filename)
    test_text = request.form['text']
    print(test_text)

    ret['status'] = 'ok'
    return ret
    

@mod.route('/upload/md', methods = ['POST'])
def uploadMd():
    pass