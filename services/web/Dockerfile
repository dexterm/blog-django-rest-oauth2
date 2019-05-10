###########
# BUILDER #
###########

# Base Image
FROM python:3.6 as builder

#########
# FINAL #
#########

# Base Image
FROM python:3.6-slim

# ----- NEW ----
# Install curl
RUN apt-get update && apt-get install -y \
    build-essential \
    mysql-client \
    python-mysqldb \
    python3-mysqldb \
    python3-dev \
    libpython3-dev \
    #libmysqlclient-dev \
    libpng-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    locales \
    zip \
    jpegoptim optipng pngquant gifsicle \
    vim \
    unzip \
    git \
    curl \
    libpq-dev \
    python-dev

#####setup virtualenv for python if required ####
#RUN pip install virtualenv
#RUN virtualenv -p python3.6 virtual
#RUN /bin/bash -c "source /virtual/bin/activate"
#####setup virtualenv for python if required ####

# Install Requirements
COPY requirements.txt /
#RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt
RUN pip install -r requirements.txt

# Create directory for the app user
RUN mkdir -p /home/project

# Create the app user
RUN groupadd app && useradd -g app app

# Create the home directory
ENV HOME=/home/project
#location inside the container, where the django python files will reside, change it to a folder of your choice
ENV APP_HOME=/home/project/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Install Requirements
#COPY --from=builder /wheels /wheels
#COPY --from=builder requirements.txt .
#RUN pip install --no-cache /wheels/*

# Copy in the Django code
COPY . $APP_HOME

# Chown all the files to the app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app

# expose the port 8000
EXPOSE 8000

# run server
#since wsgi.py resides inside blogoauth2 folder and the application service is started from level outside
# that is from the location where manage.py is located in such cases --chdir must be used
# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "blogoauth2", "--bind", ":8000", "blogoauth2.wsgi:application"]
