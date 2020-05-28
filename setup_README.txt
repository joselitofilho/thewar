# Version Manager

### Running in docker container

#### - Setup Docker
___
![](https://www.tatvasoft.com/blog/wp-content/uploads/2017/05/Docker.png)

- [Official docs](https://docs.docker.com/get-docker/)
- [How to install in Fedora](https://docs.docker.com/engine/install/fedora/)
- [How to install in MacOS](https://docs.docker.com/docker-for-mac/install/)
- [How to install in Windows](https://docs.docker.com/docker-for-windows/install/)

#### - Use docker without sudo
___
```
$ sudo usermod -aG docker ${USER}
```

#### - Setup docker-compose
___
![](https://miro.medium.com/proxy/0*lQHBTNViWBhPsTtF.)

- [How to install docker compose](https://docs.docker.com/compose/install/)

#### - Setup and running the application in development
___
```
$ docker-compose up -d --build
```

#### - Setup and running the application in production (nginx and jogowar
___
```
$ docker-compose -f docker-compose.prod.yml up
$ docker-compose down -t 1 # (Only stop)
```
