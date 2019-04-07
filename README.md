# face-recognition
This project is about Facial Recognition webservices through RestFul API that has been developed under the SRM Institute of Science and Technology B.Tech 2015 curriculum as Major project for final semester, 2019. Our team has implemented this webservices for enhancing the banking security through facial recognition with deep learning.

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

## Client examples: 
- [Php POST with CUrl](https://stackoverflow.com/questions/3433542/curl-php-send-image)
