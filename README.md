# Photos

REST API application to perform CRUD operations with photos with JWT authentication in Python using Django Framework

## API
---------

NOTE: All endpoints to get/post/edit/delete etc. photos reqiure JWT token attached to the reqest to run 
For more info, go to [JWT](https://github.com/jpadilla/django-rest-framework-jwt)

i. Post a photo

    Endpoint            : /photos/ 
    Request Type 	    : POST

ii. Edit a photo captions

    Endpoint            : /photos/{id} 
    Request Type 	    : PUT

iii. Delete a photo

    Endpoint            : /photos/{id} 
    Request Type 	    : DELETE    

iv. List photos (all, my photos, my draft)

    Endpoint (all)      : /photos/ 
    Endpoint (my photo) : /photos/my_photos/ 
    Endpoint (my draft) : /photos/my_drafts/
    Request Type 	    : GET 

v.  Sort photos by data

    Endpoint (ASC)      : /photos/?ordering=created
    Endpoint (DESC)     : /photos/?ordering=-created
    Request Type 	    : GET 

vi. Filter photos by user

    Endpoint            : /photos/?user={userid} 
    Request Type 	    : GET 
  
vii. Register user

    Endpoint            : /api/user/create/
    Request Type 	    : POST 
    Request Params 	    : username, password

viii. Get JWT token

    Endpoint            : /api/token/obtain/
    Request Type 	    : POST 
    Request Params 	    : username, password

ix. Refresh JWT token

    Endpoint            : /api/token/refresh/
    Request Type 	    : POST 
    Request Params 	    : refresh (token)

## Getting Started
---------

Run the following command inside photo_project directory to start the app locally

```
python manage.py runserver 
```

### Create super user
---------

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## TODOs

- Resize/crop image 
- Batch upload 
- Support of tags

## Deployment
---------

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
