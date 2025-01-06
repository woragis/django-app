# Django Project

## Docker commands

### Docker quickstart

Start Containers

```
docker-compose build
docker-compose up -d
```

Updated Dockerfile or docker-compose.yml

```
docker-compose up --build
```

Update database

```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

Stopping the containers

```
docker-compose down
```

See logs

```
docker-compose logs
```

See logs in real-time

```
docker-compose logs -f
```

### Controlling commands

- docker images # shows locally downloaded images
- docker ps # show running images
- docker ps -a # shows running or stopped images
- docker exec -it _containerName_ _/path_ # enters interactive state with the container image
- docker stop _name_
- docker rm _name_ # removes container
- docker rmi _name_ # removes locally downloaded image
- docker build -t my_app:1.0

### Download commands

- docker pull redis # downloads image

### Run commands

- docker run redis # downloads and runs image
- docker run redis -d # downloads and runs image without locking terminal
- docker run redis -d -p:6000:6379 # configures my computer port (6000) to the container port (6379)
- docker run redis --name _containerName_ # downloads and runs image
- --net _networkName_
- -e _ENVIRONMENTVARIABLE_

### Docker Compose

```
version: "3"
services:
  python:
    image: python
    ports: 8000:8000
  database:
    image: postgres
  cache:
    image: redis
networks: oi
```

### Dockerfile

```
FROM python

RUN mkdir -p /home/app

COPY . /home/app

RUN source /home/app/.venv/bin/activate
RUN python /home/app/.venv/bin/activate

CMD ["python", "/home/app/manage.py", "runserver"]
```
