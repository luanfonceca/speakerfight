install:
	pip install -r requirements.txt

loaddata:
	python manage.py loaddata deck/fixtures/user.json
	python manage.py loaddata deck/fixtures/event.json
	python manage.py loaddata deck/fixtures/proposal.json
	python manage.py loaddata deck/fixtures/socialapp.json

db:
	python manage.py migrate

setup: install db loaddata
