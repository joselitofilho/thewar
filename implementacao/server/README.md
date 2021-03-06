### Configure o email do jogo
```sh
$ cp implementacao/server/src/email.conf.template implementacao/server/src/email.conf
{
    "server": "smtp.gmail.com",
    "port": 587,
    "email": "",
    "password": ""
}
```

### docker-compose

###### Start the game
```sh
$ docker-compose up -d
$ docker-compose exec server bash -c "./start_game.dev.sh"
```
```sh
$ google-chrome http://localhost:9092
```

###### Access database
```sh
$ docker-compose exec server bash -c "sqlite3 war.db"
```


### Challenges

###### Generate challenges
```sh
$ docker-compose exec server bash -c "./gerar_desafio.sh"
```

### Donations

###### Configure donations goal
```sh
$ docker-compose exec server bash -c "sqlite3 war.db"
sqlite> INSERT OR REPLACE INTO Configuracoes (chave, valor) VALUES ('meta_doacao', '300');
```


### Como instalar em sua máquina

###### Install in python:
```sh
$ apt-get install python-dev
$ apt-get install python-setuptools
$ easy_install simplejson
$ # easy_install autobahn-0.5.14-py2.7.egg
$ easy_install "autobahn==19.11.2"
$ easy_install discover
$ easy_install coverage
$ cd modules-extras/pysha3-0.3/ && python setup.py install && cd ../../
$ apt-get install sqlite3
$ apt-get install redis-server
$ easy_install redis 
$ apt-get install screen
```

### Ferramenta para edição de mapas:
    - http://www.birdtheme.org/useful/v3tool.html
    - http://www.birdtheme.org/useful/editkmlfilev3.php?lake=Aral%2C+Black+and+Caspian+Sea
    - Plotar pontos: http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/encodeForm.html
    - Plotar pontos: http://people.ucsc.edu/~pbuzbee/maps/
    - Paises: http://www.dyngeometry.com/web/WorldRegion.aspx
    - Mapa Estilizado: http://gmaps-samples-v3.googlecode.com/svn/trunk/styledmaps/wizard/index.html
    - Gerador de sprite: http://pt.spritegen.website-performance.org/
    - drop-shadow: http://css3gen.com/box-shadow/
    - linear-gradient: http://www.css3factory.com/linear-gradients/
    - Material icons: https://material.io/resources/icons/?search=eye&icon=visibility&style=outline

### Sons:
    - http://www.freesound.org/
