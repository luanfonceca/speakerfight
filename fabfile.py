# coding: utf-8

from os import environ
from fabric.api import env, cd, run
from fabric.colors import yellow, green


REPOSITORY = 'git@github.com:luanfonceca/speakerfight.git'
REMOTE = 'origin'
BRANCH = 'master'
env.hosts = ['speakerfight.com']
env.user = 'root'
env.password = environ.get('PASSWORD')
env.app_dir = '/home/speakerfight'
env.project_name = 'speakerfight'
env.virtualenv_dir = '/home/virtualenv'


def _run(command, pip='python'):
    run('{venv}/bin/{target} {command}'.format(
        venv=env.virtualenv_dir,
        command=command,
        target=pip))


def _update_app():
    with cd(env.app_dir):
        print yellow('Fetch the Code')
        run('git pull {remote} {branch}'.format(
            remote=REMOTE,
            branch=BRANCH))

        print yellow('Update the Python Requirements')
        _run('install -r requirements.txt --quiet', 'pip')

        print yellow('Cleanning the .pyc files')
        _run('manage.py clean_pyc')

        print yellow('Migrate the DB')
        _run('manage.py migrate --noinput --verbosity=0')

        print yellow('Collecting the static files')
        _run('manage.py collectstatic --noinput --verbosity=0')

        print yellow('Compiling the strings')
        _run('manage.py compilemessages')

        print green('App succefully updated')


def _restart_app():
    print yellow('Restart the Uwsgi')
    run('service uwsgi restart')

    print yellow('Restart the Nginx')
    run('service nginx restart')

    print green('Services succefully restarted')


def deploy():
    _update_app()
    _restart_app()
    print green('Deploy succefully done!')


def load_initial_data():
    fixtures = [
        'deck/fixtures/user.json',
        'deck/fixtures/event.json',
        'deck/fixtures/proposal.json',
    ]
    with cd(env.app_dir):
        print yellow('Collecting the initial data')
        for fixture in fixtures:
            _run('manage.py loaddata {}'.format(fixture))
        print green('Data succefully loaded')
