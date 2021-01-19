
#########
# Multistage docker build
####
#                         
#  python:3.8.0 | --> base1 |--> gbdevel
#                           |--> gbweb  
#
#
#


FROM python:3.8.0 as base1

# Prevent python from writing pyc files to disk
ENV PHTHONDONTWRITEBYTECODE 1
# Prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
   # for entrypoint shell script
   netcat \
   # pillow dependencies  *** I don't think we are using pillow now
   qt5-default \
   libwebkit2gtk-4.0-37 \
   libxss1 \
   iputils-ping \
   # Psycopg2 dependencies
   libpq-dev python3-dev \
   # Other
   ffmpeg \
   # for development
   vim curl net-tools dumb-init

RUN python -m pip install --upgrade pip
WORKDIR /opt/setup
COPY ./serverapp/requirements.txt /opt/setup/requirements.txt
RUN python -m pip install -r requirements.txt

#####################################################
#### build the container to do development and test
#####################################################
FROM base1 as gbdevel
# this is a container to be used for for development and system tests
# This is not implemented yet.  TODO when docker-compose profiles comes
# This will be easier to implement
RUN python -m pip install pytest
WORKDIR /opt/serverapp

#####################################################
#### build the container for the webservice
#####################################################
FROM base1 as gbweb

COPY ./devel/entrypoint.sh /opt/setup/entrypoint.sh
COPY ./devel/command.sh /opt/setup/command.sh
WORKDIR /opt/serverapp


ENTRYPOINT ["/opt/setup/entrypoint.sh"]