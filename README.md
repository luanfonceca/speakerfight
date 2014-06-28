speakerfight
============

Speakerfight is an arena where the Speakers can fight each other and the people choose who wins.

[![Code Health](http://waffle2shields.herokuapp.com/landscape/?user=luanfonceca&repo=speakerfight&branch=master&label=health&style=flat)](https://landscape.io/github/luanfonceca/speakerfight/master) [![Github Issues](http://img.shields.io/github/issues/luanfonceca/speakerfight.svg?style=flat)](https://github.com/luanfonceca/speakerfight/issues?sort=updated&state=open) [![Stories in Ready](http://waffle2shields.herokuapp.com/waffle/?user=luanfonceca&repo=speakerfight&label=ready&style=flat)](https://waffle.io/luanfonceca/speakerfight) [![Build Status](http://img.shields.io/travis/luanfonceca/speakerfight.svg?branch=master&style=flat)](https://travis-ci.org/luanfonceca/speakerfight) [![Coverage Status](http://img.shields.io/coveralls/luanfonceca/speakerfight.svg?branch=master&style=flat)](https://coveralls.io/r/luanfonceca/speakerfight?branch=master)

============
### Install and Run
```sh
$ git clone git@github.com:luanfonceca/speakerfight.git
$ cd speakerfight
$ pip install -r requiremets.txt
$ python manage.py syncdb --migrate # we have a fixture for the users...
$ python manage.py loaddata deck/fixtures/user.json 
# username: admin, password: admin; 
# username: user, password: user
$ python manage.py loaddata deck/fixtures/event.json
$ python manage.py loaddata deck/fixtures/proposal.json
$ python manage.py runserver
Validating models...

0 errors found
          ...
Django version 1.6.2, using settings 'settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
