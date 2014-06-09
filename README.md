speakerfight
============

Speakerfight is an arena where the Speakers can fight each other and the people choose who wins.

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
