help:
	@echo "coverage-console - run code coverage and output to console"
	@echo "coverage-html - run code coverage and output to HTML"
	@echo "db - create and migrate database"
	@echo "install - install Python dependencies"
	@echo "loaddata - load initial data"
	@echo "setup - prepare development environment"
	@echo "test - run tests"

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

test:
	./manage.py test

coverage:
	coverage erase
	coverage run ./manage.py test

coverage-console: coverage
	coverage report -m

coverage-html: coverage
	coverage html
