# blog-django-rest-oauth2
Boiler plate for getting started with django using docker-compose

## What will you need
Docker, docker-compose, python3.6, django, django-restframework, django-oauth-toolkit

### Install docker and docker-compose
### How To Install and Use Docker on Ubuntu 18.04
https://linuxize.com/post/how-to-install-and-use-docker-on-ubuntu-18-04/
### How To Install and Use Docker Compose on Ubuntu 18.04
https://linuxize.com/post/how-to-install-and-use-docker-compose-on-ubuntu-18-04/

### For ease of readability the docker-compose environment variables have been stored in separate .env files

### Start the docker containers
Reference http://pawamoy.github.io/2018/02/01/docker-compose-django-postgres-nginx.html
```
docker-compose up
```
**or**
```
docker-compose up -d
```
**docker-compose up -d [runs in detached mode or in background, allowing you to use the terminal window for other tasks]**

### Test postgresql connection from host system
```
docker exec -it pgdb  psql -h pgdb -U django -d my_project
Syntax:
 docker exec -it <service_name> psql -h <postgres_service_name> -U <POSTGRES_USER> -d <POSTGRES_DB>
```

### Verify phpMyAdmin
```
phpMyAdmin service is configured on port 8001
Point your browser to http://localhost:8001
The username and password is stored in file services/mysql/.env
```
### Verify pgMyAdmin
pgMyAdmin service is configured on port 8002
```
Point your browser to http://localhost:8002
The username and password is stored in file services/pgsql/.env
```

### Verify django is running
Django is configured to run on port 8000, nginx routes the request via port 80
```
Point your browser to http://localhost
```
You should be presented with the Django welcome page
"The install worked successfully! Congratulations!"

### MIGRATE THE DATABASE
```
docker exec -it djangoapp  python manage.py makemigrations
docker exec -it djangoapp  python manage.py migrate
```
### OVERHAULING/REFACTORING TABLES may create issues with makemigrations
If you experience with above commands migrating the database due to frequent alterations to any of the models, then simply clear
all the migration scripts and drop the database using these test_commands
```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
docker-compose down -v data-volume-pg
docker-compose down -v data-volume-mysql
```
The above commands will find and delete all migration scripts, the docker-compose down -v will erase the volume and new volume
will be created when docker-compose up is executed

### SETUP SUPERUSER
```
docker exec -it djangoapp  python manage.py createsuperuser
```
### SETUP REGULAR USER
```
docker exec -it djangoapp  python manage.py createuser <username> <email> <password>
```
or create usertype admin
```
docker exec -it djangoapp  python manage.py createuser <username> <email> <password> --admin
```
or create usertype admin and staff
```
docker exec -it djangoapp  python manage.py createuser <username> <email> <password> --admin --staff
```
or create usertype staff
```
docker exec -it djangoapp  python manage.py createuser <username> <email> <password> --staff
```

### STRUCTURE tests
```
└── app_name
    └── tests
        ├── __init__.py
        ├── test_forms.py
        ├── test_commands.py
        ├── test_models.py
        └── test_views.py
```        

### If you get an error
log.Category.created_by: (fields.E301) Field defines a relation with the model 'auth.User', which has been swapped out.
	HINT: Update the relation to point at 'settings.AUTH_USER_MODEL'.
simply replace   settings.AUTH_USER_MODEL with users.User
replace this code
```
updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='+')
```
WITH
```
from users.User import User as customUser
models.ForeignKey(customUser, null=True, on_delete=models.CASCADE, related_name='+')
```
### Check if admin page is rendered proplery
point your browser to http://localhost/admin
If the page is not rendered properly, it could be because the folder static is not mapped inside the container
run below command to generate static files into /home/project/web/static
```
docker exec -it djangoapp python manage.py collectstatic
```

   ### Use curl to test api end points
   For this an oauth client id and client secret must be created
   Point your browser to http://localhost/o/applications
   Click the button "New application"

   In the form that follows fill in the following details

   name: Any name that you wish to identify the application with ex: webapi

   client id and client secret should not be modified, leave as is

   client type: Select "confidential" from the dropdown list

   Authorization Grant Type: Select "Resource owner password based" from the drop down list

   Make note or copy the client id and secret it will be required for generating tokens

   Finally click the save button

#### Generate a token
Assuming you have created a superuser or regular user, in the command below replace with your credentials
```
curl -X POST -d "grant_type=password&username=joh&password=john&scope=read" -u"AlwzTR73kuJnS9RIUHKDmPaWATBnk5AUXpFhZdbR:6kDPkSp63ZQnrqfV41rheUxyyclWeLyZNDtphTQWLja4rM2UyKJsLKNBky43zhf5ZyEYwHVCvN89VxAp6jNnd0eyHi70I2gFueZ3QUVCgYjl2T69X0BhuuQ8kYU13Lpq" http://localhost/o/token/
```
You should receive a response similar to this
{"access_token": "T8ppcqd8U3BFrvONyd6Hxi8FzMLYxh", "expires_in": 36000, "token_type": "Bearer", "scope": "read", "refresh_token": "LV1J8aZCfutGt5fUA1dk6tYRvIfryy"}
Make note or copy the access_token value : T8ppcqd8U3BFrvONyd6Hxi8FzMLYxh
This token must be passed with every curl or api request

#### Create a new post using curl POST method
```
curl   -H "Authorization: Bearer xpvpU6eNmL1yajNbP3pM3APWU2dmkG" -X POST   -H 'Content-Type: application/json' -d '{"title":"Performance considerations for calculated_fields","content":"With either of the above approaches, you would be running two exta queries per object (One per calculated field). You can find how to optimize this in How to optimize queries in Django admin?.",  "slug":"112oops-in-rust1`2", "categories":[{"id":3, "title":"RUST"}], "tags":[{"id":1, "title":"RUST"},{"id":2,"title":"python"}, {"id":3,"title":"django"}], "pstatus":"AP"}'  http://localhost/api/v1/posts/
```
If there was no error then you should receive a response similar to : {"id":1,"content":"Performance considerations for calculated_fields","cstatus":"AP","created_at":"2019-05-19T11:59:29.723000Z"}

There are three models in blog/models.py  

Post , Category and Comment

A post can belong to multiple categories and a category can have many posts. A post can have multiple comments,
but a comment must belong to one post only. Check the models.py to see the relationships, and how properties are set
and retrieved.

#### Fetch all posts using curl GET method
```
curl   -H "Authorization: Bearer T8ppcqd8U3BFrvONyd6Hxi8FzMLYxh"  http://localhost/api/v1/posts/
```

#### Create a new comment using curl POST method
```
curl   -H "Authorization: Bearer T8ppcqd8U3BFrvONyd6Hxi8FzMLYxh" -X POST   -H 'Content-Type: application/json' -d '{"content":"My first comment...",  "cstatus":"AP",  "post_id":1 }'  http://localhost/api/v1/comments/
```
If there was no error then you should receive a response similar to : {"id":1,"content":"My first comment..."}

#### Fetch all comments using curl GET method
```
curl   -H "Authorization: Bearer T8ppcqd8U3BFrvONyd6Hxi8FzMLYxh"  http://localhost/api/v1/comments/
```
