# coding: utf-8

from fabric.api import env, cd, run, sudo
from fabric.contrib.files import exists
from fabric.colors import yellow, green


REPOSITORY = 'git@github.com:luanfonceca/speakerfight.git'
REMOTE = 'origin'
BRANCH = 'master'
env.hosts = ['speakerfight.com']
env.user = 'root'
env.app_dir = 'speakerfight'
env.project_name = 'speakerfight'
env.virtualenv_dir = '~/.virtualenvs'


def _create_ve(project_name):
    print yellow('Installing Virtualenv')
    sudo('apt-get install python-virtualenv')
    if not exists(env.virtualenv_dir):
        print yellow('Creating the Virtualenv folder')
        run('mkdir {venv}'.format(venv=env.virtualenv_dir))
    if not exists('/'.join([env.virtualenv_dir, project_name])):
        with cd(env.virtualenv_dir):
            print yellow('Creating the Virtualenv')
            run('virtualenv {0}'.format(project_name))
            print green('Virtualenv succefully created')
    else:
        print 'Virtualenv {0} already exists, skipping...'.format(
            env.project_name)


def _run(command, pip=''):
    run('{venv}/{project_name}/bin/{target} {command}'.format(
        venv=env.virtualenv_dir,
        project_name=env.project_name,
        command=command,
        target=pip or 'python'))


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

    print yellow('Restart the Supervisor')
    sudo('supervisorctl restart {project_name}'.format(**env))

    print green('Services succefully restarted')


def deploy():
    _update_app()
    _restart_app()
    print green('Deploy succefully done!')


def setup_nginx():
    if not run('which nginx'):
        print yellow('Installing Nginx')
        sudo('apt-get install nginx')
    with cd('/etc/nginx/sites-enabled/'):
        sudo('touch {0}'.format(env.project_name))
        with open('nginx') as nginx:
            text = ''.join(nginx.readlines()).format(
                host=env.hosts[0],
                user=env.user,
                project_name=env.project_name)
            sudo("echo '{0}' > {1}".format(text, env.project_name))


def setup_supervisor():
    if not run('which supervisorctl'):
        print 'Installing Supervisor'
        sudo('apt-get install supervisor')
    with cd('/etc/supervisor/conf.d/'):
        sudo('touch {0}.conf'.format(env.project_name))
        with open('supervisor') as supervisor:
            text = ''.join(supervisor.readlines()).format(
                project_name=env.project_name,
                user=env.user)
            sudo("echo '{0}' > {1}.conf". format(text, env.project_name))
    sudo("supervisorctl reload")


def bootstrap():
    print yellow('Update the system packages.')
    sudo('apt-get update')
    sudo('apt-get install build-essential python python-dev')

    _create_ve(env.project_name)
    if not exists('~/{0}'.format(env.project_name)):
        print yellow('Get the Code.')
        run('git clone {0}'.format(REPOSITORY))
    setup_nginx()
    setup_supervisor()
    _update_app()
    _restart_app()
    print green('Bootstrap succefully done!')
