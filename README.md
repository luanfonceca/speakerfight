speakerfight
============

[![Join the chat at https://gitter.im/luanfonceca/speakerfight](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/luanfonceca/speakerfight?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Beerpay](https://beerpay.io/luanfonceca/speakerfight/badge.svg?style=flat)](https://beerpay.io/luanfonceca/speakerfight) 

Speakerfight is an arena where speakers can fight ~against~ each other and people choose who wins.

[![Code Health](https://landscape.io/github/luanfonceca/speakerfight/master/landscape.svg?style=flat)](https://landscape.io/github/luanfonceca/speakerfight/master) [![Github Issues](http://img.shields.io/github/issues/luanfonceca/speakerfight.svg?style=flat)](https://github.com/luanfonceca/speakerfight/issues?sort=updated&state=open) [![Build Status](http://img.shields.io/travis/luanfonceca/speakerfight.svg?branch=master&style=flat)](https://travis-ci.org/luanfonceca/speakerfight) [![Coverage Status](http://img.shields.io/coveralls/luanfonceca/speakerfight.svg?branch=master&style=flat)](https://coveralls.io/r/luanfonceca/speakerfight?branch=master)

============
### Install

#### Normal installation
```sh
$ git clone git@github.com:luanfonceca/speakerfight.git
$ cd speakerfight
$ pip install -r requirements.txt
$ make setup # we have a fixture for the users...
# username: admin, password: admin;
# username: user, password: user
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
$ docker-compose run web make setup # we have a fixture for the users...
# username: admin, password: admin;
# username: user, password: user
$ docker-compose up
