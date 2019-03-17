# face-recognition

## Installation
Linux Ubuntu 18.04 LTS
```
$ git clone https://github.com/10zinten/face-recognition.git
$ cd face-recognition
$ virtualenv env -p python3.6$ 
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Usage
Start the server
```
$ cd app
$ python api.py
```

User registeration:
```
$ curl -X POST -F "image=@<path-to-image>" -F "userid=<userid>" http://0.0.0.0:8000/register
{'Status': true}  #returned json
```

user authentication:
```
$ curl -X POST -F "image=@<path-to-image>" -F "userid=<userid>" http://0.0.0.0:8000/auth
{'auth_status': true, 'upload_data': true, 'user_id': <userid>}  #returned json
```
