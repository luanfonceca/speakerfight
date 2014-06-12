import multiprocessing

user = "root"
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
pidfile = "/tmp/speakerfight.pid"
name = "speakerfight"
backlog = 2048
logfile = "/{user}/log/gunicorn.{name}.log".format(
    user=user, name=name)
