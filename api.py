from pathlib import Path

from flask import Flask, request, Response, render_template
import jsonpickle
import face_recognition
import numpy as np

app = Flask(__name__)

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
        user_dir = Path('auth') / userid
        user_dir.mkdir(parents=True, exist_ok=True)
        if len(list(user_dir.iterdir())):
            response = {
                'Status': False
            }
        else:
            # create encoding of the face image and store
            img = face_recognition.load_image_file(file_obj)
            encoding = face_recognition.face_encodings(img)[0]
            np.save(str(user_dir / '{}_encoding'.format(userid)), encoding)
            response = {
                'Satus': True
            }
        
    response_pickled = jsonpickle.encode(response)

    return Response(response_pickled, status =200, mimetype="application/json")


def is_authenticate(userid, file_obj):
    user_dir = Path('auth') / userid
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
