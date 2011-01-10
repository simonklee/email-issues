from fabric.api import run, env, sudo
from fabric.context_managers import cd
from fabric.utils import abort

env.hosts = ['localhost']
proj_root = '/home/simon/src/mail-notify'

def on_path(path=proj_root):
    def deco(func):
        def _wrapper():
            with cd(path):
                return func()
        return _wrapper
    return deco

@on_path()
def pull_master():
    run('git pull --ff origin master')

def pull_last_tag():
    run('git fetch --tags')
    tags = run('git tag')
    try:
        tag = tags.split()[-1:][0]
        run('git merge %s --ff' % tag)
    except IndexError:
        abort('no tags available')

@on_path()
def update_dependencies():
    run('contrib/bootstrap.py')

@on_path()
def deploy():
    run('ls -lah')
