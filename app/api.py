import os
from flask import Flask, request, Response
import jsonpickle
import face_recognition
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    # add usage of API and possibly access key
    pass


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        file_obj = request.files['image']
        userid = request.form['userid']

        # create dir with name userid in auth/ to store the face_encoding.
        user_dir = os.path.join('auth', userid)
        if os.listdir(user_dir):
            response = {
                'Status': False
            }
        else:
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            img = face_recognition.load_image_file(file_obj)
            encoding = face_recognition.face_encodings(img)[0]
            np.save(os.path.join(user_dir, '{}_encoding'.format(userid)), encoding)
            response = {
                'Satus': True
            }
        
    response_pickled = jsonpickle.encode(response)

    return Response(response_pickled, status =200, mimetype="application/json")


def is_authenticate(userid, file_obj):
    user_dir = os.path.join('auth', userid)
    src_encoding_fn = os.path.join(user_dir, '{}_encoding.npy'.format(userid))
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

        if file_obj and userid:
            response = {
                'upload_data': True,
                'userid': userid,
                'auth_status': is_authenticate(userid, file_obj),
            }
        else:
            response = {
                'upload_data': False,
                'userid': userid,
                'auth_status': False
            }

        response_pickled = jsonpickle.encode(response)

        return Response(response_pickled, status =200, mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)