from web.db.datamodels import *
from web.db.databases import db_session
from sqlalchemy import func

class GetPhotos():
    def __call__(self, user_name, album_name = None):
        db_session_instance = db_session()
        if album_name is None:
            album_list = db_session_instance\
                .query(Album).join(User)\
                .filter(User.user_name == user_name)\
                .all()
        else:
            album_list = db_session_instance\
                .query(Album).join(User)\
                .filter(User.user_name == user_name, Album.album_title == album_name)\
                .all()

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

class GetFolderDetail():
    def __call__(self, user_id):
        db_session_instance = db_session()
        return_posts = []

        folders = db_session_instance\
            .query(Folder).join(User)\
            .filter(User.ID == user_id)\
            .all()
        for folder in folders:
            folder_id = folder.ID
            folder_title = folder.folder_title
            create_time = folder.create_time
            folder_dict = dict()
            folder_dict['title'] = str(folder_title)
            folder_dict['createdTime'] = create_time
            folder_dict['posts'] = []
            posts = db_session_instance\
                .query(Post, func.count(Comment.ID)).outerjoin(Comment)\
                .filter(Post.folder_ID == folder_id)\
                .group_by(Post.ID)\
                .all()
            for post, comment_num in posts:
                post_dict = dict()
                star_num = db_session_instance\
                    .query(func.count(Star.user_id)).outerjoin(Post)\
                    .filter(Star.post_id == post.ID)\
                    .group_by(Star.post_id)\
                    .first()
                post_dict['title'] = post.post_title
                post_dict['createTime'] = post.create_time
                post_dict['format'] = post.document_format
                post_dict['id'] = post.ID   
                post_dict['published'] = post.is_published
                post_dict['stars'] = star_num
                post_dict['comments'] = comment_num
                folder_dict['posts'].append(post_dict)
            return_posts.append(folder_dict)
        return return_posts

class GetFolder():
    def __call__(self, user_id):
        db_session_instance = db_session()
        return_posts = []

        folders = db_session_instance\
            .query(Folder.ID, Folder.folder_title).join(User)\
            .filter(User.ID == user_id)\
            .all()
        for folder in folders:
            folder_id = folder.ID
            folder_title = folder.folder_title
            folder_dict = dict()
            folder_dict['title'] = str(folder_title)
            folder_dict['posts'] = []

            posts = db_session_instance\
                .query(Post.post_title)\
                .filter(Post.folder_ID == folder_id)\
                .all()
            for post in posts:
                post_dict = dict()
                post_dict['title'] = post.post_title
                folder_dict['posts'].append(post_dict)
            return_posts.append(folder_dict)
        return return_posts

class GetPost():
    def __call__(self, user_name, folder_name, post_title):
        db_session_instance = db_session()
        return_post = dict()

        post = db_session_instance\
            .query(Post).join(Folder).join(User)\
            .filter(User.user_name == user_name).filter(Folder.folder_title == folder_name).filter(Post.post_title == post_title)\
            .first()

        if post is None:
            return None

        else:
            star_num = db_session_instance\
                .query(func.count(Star.user_id)).outerjoin(Post)\
                .filter(Star.post_id == post.ID)\
                .group_by(Star.post_id)\
                .first()
            return_post['title'] = post.post_title
            return_post['createTime'] = post.create_time
            return_post['content'] = post.post_content
            return_post['format'] = post.document_format
            return_post['postID'] = post.ID
            return_post['stars'] = star_num
            return_post['published'] = post.is_published

            comments = db_session_instance\
                .query(Comment, User.user_name).join(Post)\
                .filter(Post.ID == post.ID).filter(User.ID == Comment.user_id)\
                .all()
            comment_list = []
            for c, u in comments:
                comment = dict()
                comment['username'] = str(u)
                comment['comment'] = c.content
                comment['time'] = c.create_time
                comment_list.append(comment)
            return_post['comments'] = comment_list
 
            return return_post
