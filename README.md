speakerfight
============

[![Join the chat at https://gitter.im/luanfonceca/speakerfight](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/luanfonceca/speakerfight?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Speakerfight is an arena where speakers can fight ~against~ each other and people choose who wins.

[![Code Health](https://landscape.io/github/luanfonceca/speakerfight/master/landscape.svg?style=flat)](https://landscape.io/github/luanfonceca/speakerfight/master) [![Github Issues](http://img.shields.io/github/issues/luanfonceca/speakerfight.svg?style=flat)](https://github.com/luanfonceca/speakerfight/issues?sort=updated&state=open) [![Stories in Ready](http://waffle2shields.herokuapp.com/waffle/?user=luanfonceca&repo=speakerfight&label=ready&style=flat)](https://waffle.io/luanfonceca/speakerfight) [![Build Status](http://img.shields.io/travis/luanfonceca/speakerfight.svg?branch=master&style=flat)](https://travis-ci.org/luanfonceca/speakerfight) [![Coverage Status](http://img.shields.io/coveralls/luanfonceca/speakerfight.svg?branch=master&style=flat)](https://coveralls.io/r/luanfonceca/speakerfight?branch=master)

============
### Install

#### Normal installation
```sh
$ git clone git@github.com:luanfonceca/speakerfight.git
$ cd speakerfight
$ make setup
$ python manage.py runserver
```

#### Using Docker
Dependecies
- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)

```sh
$ git clone git@github.com:luanfonceca/speakerfight.git
$ cd speakerfight
$ docker-compose build
$ docker-compose run web python manage.py migrate # we have a fixture for the users...
$ docker-compose run web python manage.py loaddata deck/fixtures/user.json
# username: admin, password: admin;
# username: user, password: user
$ docker-compose run web python manage.py loaddata deck/fixtures/event.json
$ docker-compose run web python manage.py loaddata deck/fixtures/proposal.json
$ docker-compose run web python manage.py loaddata deck/fixtures/socialapp.json
$ docker-compose up
```
