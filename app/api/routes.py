from pathlib import Path

from flask import request, Response, render_template
import face_recognition
import jsonpickle
import numpy as np

from api import app
from api import db
from api.models import User


REGISTRATION = 'registration'
AUTH = 'auth'
TEST = 'test'
FAILED = 'failed'
SUCCEED = 'succeed'
EMBEDDINGS_PATH = Path('api/embeddings').resolve()


@app.route("/")
def index():
    # add usage of API and possibly access key
    return render_template('index.html')


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        file_obj = request.files['image']
        userid = request.form['userid']
 
        # create dir with name userid in auth/ to store the face_encoding.
        user_dir = EMBEDDINGS_PATH / userid
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # check if userid already exists
        if User.query.filter_by(userid=userid).first():
            response = {
                'type': REGISTRATION,
                'userid': userid,
                'status': FAILED
            }
        else:
            # add user to database
            user = User(userid=userid)
            db.session.add(user)
            db.session.commit()
            
            # create encoding of the face image and store
            img = face_recognition.load_image_file(file_obj)
            encoding = face_recognition.face_encodings(img)[0]
            np.save(str(user_dir / '{}_encoding'.format(userid)), encoding)
            response = {
                'type': REGISTRATION,
                'userid': userid,
                'status': SUCCEED
            }
        
    response_pickled = jsonpickle.encode(response)

    return Response(response_pickled, status =200, mimetype="application/json")


def is_authenticate(userid, file_obj):
    user_dir = EMBEDDINGS_PATH / userid
    src_encoding_fn = str(user_dir / '{}_encoding.npy'.format(userid))
    src_encoding = np.load(src_encoding_fn)

    img = face_recognition.load_image_file(file_obj)
    encoding = face_recognition.face_encodings(img)[0]

    result = face_recognition.compare_faces([src_encoding], encoding)[0]

    return bool(result)


@app.route("/auth", methods=["POST"])
def authenticate():
    if request.method == "POST":
        file_obj = request.files['image']
        userid = request.form['userid']

        if file_obj and userid and User.query.filter_by(userid=userid).first():
            response = {
                'type': AUTH,
                'data_received': SUCCEED,
                'userid': userid,
                'status': SUCCEED if is_authenticate(userid, file_obj) else FALIED
            }
        else:
            response = {
                'type': AUTH,
                'data_received': FALIED,
                'userid': userid,
                'status': FAILED
            }

        response_pickled = jsonpickle.encode(response)

        return Response(response_pickled, status =200, mimetype="application/json")


@app.route("/test", methods=["POST"])
def test():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        response = {
            'username': username,
            'status': FAILED,
            'message' : 'Hello {}, it is working !!!'.format(username)
        }

        response_pickled = jsonpickle.encode(response)

        return Response(response_pickled, status =200, mimetype="application/json")
