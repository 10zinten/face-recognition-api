# face-recognition
This project is about Facial Recognition webservices through RestFul API that has been developed under the SRM Institute of Science and Technology B.Tech 2015 curriculum as Major project for final semester, 2019. Our team has implemented this webservices for enhancing the banking security through facial recognition with deep learning.

## Installation
Linux Ubuntu 18.04 LTS
```
$ git clone https://github.com/10zinten/face-recognition.git
$ cd face-recognition-api
$ virtualenv env -p python3.6
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Usage
Start the server
```
$ cd app
$ python run.py
```

User registeration:
```
$ curl -X POST -F "image=@<path-to-image>" -F "userid=<userid>" http://0.0.0.0:8000/register
{
  "type": "registration",
  "Status": succeed/failed,
  "userid": <userid>
  "face_detected": succeed/failed
}
```

user authentication:
```
$ curl -X POST -F "image=@<path-to-image>" -F "userid=<userid>" http://0.0.0.0:8000/auth
{
  "type": "auth",
  "status": succeed/failed, 
  "data_received": succeed/failed, 
  "user_id": <userid>
  "face_detected": succeed/failed
}
```

## Client examples: 
- Php
  - [Registration](https://github.com/10zinten/face-recognition-api/blob/master/examples/php/register.php)
    ![registeration](https://github.com/10zinten/face-recognition-api/blob/master/examples/php/imgs/api_register.png)
    
  - [Authentication](https://github.com/10zinten/face-recognition-api/blob/master/examples/php/auth.php)
    ![authentication](https://github.com/10zinten/face-recognition-api/blob/master/examples/php/imgs/api_auth.png)
    !
