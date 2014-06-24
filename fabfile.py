# coding: utf-8

from os import environ
from fabric.api import env, cd, run, sudo
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
        project_name=env.project_name,
        command=command,
        target=pip))


def _update_app():
    with cd(env.app_dir):
        print yellow('Fetch the Code')
        run('git pull {remote} {branch}'.format(
            remote=REMOTE,
            branch=BRANCH))

        print yellow('Update the Python Requirements')
        _run('install -r requirements.txt', 'pip')

        print yellow('Migrate the DB')
        _run('manage.py syncdb --migrate --noinput')

        print yellow('Collecting the static files')
        _run('manage.py collectstatic --noinput')
        print green('App succefully updated')


def _restart_app():
    print yellow('Restart the Nginx')
    sudo('service nginx restart')

    print yellow('Restart the Uwsgi')
    sudo('service nginx uwsgi')

    print green('Services succefully restarted')


def deploy():
    _update_app()
    _restart_app()
    print green('Deploy succefully done!')
