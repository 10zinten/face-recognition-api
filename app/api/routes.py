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


def create_embeddings(images, user_dir):
    for i, image in enumerate(images):
        img = face_recognition.load_image_file(image)
        encoding = face_recognition.face_encodings(img)[0]
        np.save(str(user_dir / '{}_embedding'.format(i+1)), encoding)


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        images = []
        userid = request.form['userid']
 
        # create dir with name userid in auth/ to store the face_encoding.
        user_dir = EMBEDDINGS_PATH / userid
        user_dir.mkdir(parents=True, exist_ok=True)
        
        print(User.query.filter_by(userid=userid).first())

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

            # get all the user's face images
            images.append(request.files['image1'])
            images.append(request.files['image2'])
            images.append(request.files['image3'])
            images.append(request.files['image4'])
            images.append(request.files['image5'])
            

            # create embeddings of the face image and store
            try:
                create_embeddings(images, user_dir)
                response = {
                    'type': REGISTRATION,
                    'userid': userid,
                    'status': SUCCEED
                }
            except:
                response = {
                    'type': REGISTRATION,
                    'userid': userid,
                    'status': FAILED
                }

    print(response)
    response_pickled = jsonpickle.encode(response)

    return Response(response_pickled, status =200, mimetype="application/json")


def is_authenticate(userid, file_obj, thresh=4):
    user_dir = EMBEDDINGS_PATH / userid
    img = face_recognition.load_image_file(file_obj)

    try:
        encoding = face_recognition.face_encodings(img)[0]
    except:
        # No face detected, image without face
        return False

    results = []
    for i in range(5):
        src_encoding_fn = str(user_dir / '{}_embedding.npy'.format(i+1))
        src_encoding = np.load(src_encoding_fn)
        result = face_recognition.compare_faces([src_encoding], encoding)[0]
        results.append(bool(result))

    results = np.array(results)
    print(results)
    return len(results[results == True]) >= thresh


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
                'data_received': FAILED,
                'userid': userid,
                'status': FAILED
            }

        print(response)
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
