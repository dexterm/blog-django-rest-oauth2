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
In your browser open url http://localhost:8001
The username and password is stored in file services/mysql/.env
```
### Verify pgMyAdmin
pgMyAdmin service is configured on port 8002
```
In your browser open url http://localhost:8002
The username and password is stored in file services/pgsql/.env
```

### Verify django is running
Django is configured to run on port 8000, nginx routes the request via port 80
```
In your browser open url http://localhost
```
You should be presented with the Django welcome page
"The install worked successfully! Congratulations!"

### MIGRATE THE DATABASE
```
docker exec -it djangoapp  python manage.py makemigrations
docker exec -it djangoapp  python manage.py migrate
```

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
