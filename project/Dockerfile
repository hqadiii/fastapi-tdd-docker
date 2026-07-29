# pull official base image
FROM python:3.13.3-slim-bookworm

# set working firectory
WORKDIR /usr/src/app

# set enrironment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat-traditional gcc postgresql \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod uo+x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT [ "sh", "/usr/src/app/entrypoint.sh" ]