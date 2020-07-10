#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------
describe:
    Install the environment for running project

base_info:
    __version__ = "v.10"
    __author__ = "mingliang.gao"
    __time__ = "2020/5/19 3:46 PM"
    __mail__ = "mingliang.gao@163.com"
    
long description: None
--------------------------------------------------------------
"""

# ------------------------------------------------------------
# usage: /usr/bin/python install_env.py
# ------------------------------------------------------------
import sys
import os
import inspect
import shutil
from subprocess import PIPE, Popen
from platform import python_version


MAX_PYTHON_VERSION = '3'


class InstallEnv(object):
    name = 'InstallEnv'

    def __init__(self, base_dir, venv, setup, pip_requirements, py_version):
        self.root = base_dir
        self.venv = venv
        self.requirements = pip_requirements
        self.python_v = py_version
        self.setup_f = setup
        self.python = os.path.join(self.venv, 'bin/python')
        self.pip = os.path.join(self.venv, 'bin/pip')
        self.activate = os.path.join(self.venv, 'bin/activate')
        self.dist = os.path.join(self.root, 'dist')

    @staticmethod
    def print_help(venv, python):
        help = """
-----------------------------------------------------------------------
Great, Successful install the environment for running project.

Python version: %s

To activate the project virtualenv for the extent of your current shell
session you can run:

$ source %s/bin/activate

Also, make test will automatically use the virtualenv.
-----------------------------------------------------------------------
"""
        print(help % (python, venv))

    def die(self, message):
        _print_message(message, t='error')
        sys.exit(1)

    def _buildin_run_cmd(self, cmd, shell=True, check_exit_code=True, cwd=None):
        """
        execute command at shell
        :param cmd: command
        :param shell: is or not run shell
        :param check_exit_code: check is or not return code
        :param cwd: current work dir
        :return: command return code, command content
        
        cmd:
          - "ls"
          - ["ls", "-a"]
        """
        if not cwd:
            cwd = self.root
        p = Popen(cmd,
                  shell=shell,
                  bufsize=0,
                  cwd=cwd,
                  stdout=PIPE)
        output = p.communicate()[0]
        returncode = p.returncode
        if check_exit_code and returncode != 0:
            self.die('Command "%s" failed.\n%s' % (' '.join(cmd), output))
        return returncode, output

    def run_command(self, cmd, check_exit_code=True, shell=True, cwd=None):
        retcode = self._buildin_run_cmd(cmd, shell=shell, check_exit_code=check_exit_code, cwd=cwd)[0]
        return 0 if retcode in [0, '0'] else retcode

    def check_command_by_which(self, cmd):
        return True if self.run_command("which %s" % cmd, check_exit_code=False) == 0 \
            else False

    def _create_virtualenv(self):
        if self.check_command_by_which('pip'):
            _print_message("Installing virtualenv via pip......")
            if self.run_command(['pip', 'install', 'virtualenv==16.7.9'], shell=False) == 0:
                _print_message("Virtualenv is installing Success.", t="important")
                return
            else:
                self.die("ERROR: virtualenv is installing error."
                         "please install the packages to install virtualenv.")
        else:
            self.die("Pip is not found. please install pip first.")

    def check_or_create_virtualenv(self):
        self._create_virtualenv() if not self.check_command_by_which('virtualenv') \
            else _print_message('Command virtualenv is exist.')

    def check_venv(self):
        if not os.path.exists(self.venv):
            return False

        if os.path.exists(self.python):
            _print_message('Virtualenv "%s" is exist.' % self.python)
            return True
        else:
            return False

    def install_venv(self):
        _print_message("Create .venv ......")
        cmd = ['virtualenv', '-q', '--no-site-packages', '--python=python3.7', self.venv]
        _print_message('.Venv is create ok.', t='important') \
            if self.run_command(cmd, shell=False) == 0 \
            else self.die('.Venv is create failure.')

    def activate_venv_p(self):
         _print_message('Virtualenv %s activate is success.' % self.python) \
             if self.run_command("source %s" % self.activate, shell=True) == 0 \
             else self.die('Virtualenv %s activate is failure.' % self.python)

    def _pip_install_requirements(self):
        self.run_command([self.pip, 'install', '-r', self.requirements],
                         shell=False)
        _print_message('.Venv pip install -r requirements ok.')

    def del_file(self, path, dir_flag=False):
        """
        delete file and dir
        :param path: file or dir path
        :param dir_flag: is or not dir
        :return: True or False
        """
        if not os.path.exists(path):
            return

        try:
            os.remove(path) if not dir_flag else shutil.rmtree(path)
        except:
            self.die('Delete %s is failure.' % path)

    def _del_core_noneed_file(self):
        self.del_file(self.dist, dir_flag=True)

    def _pip_install_core(self):
        _print_message("Setup core package......")
        self.del_file(self.dist, dir_flag=True)
        self.run_command([self.python, self.setup_f, 'sdist'], shell=False)
        dist_dirs = os.listdir(self.dist)
        if not dist_dirs:
            self.die("Setup core package is failure.")

        core_targz = os.path.join(self.dist, dist_dirs[0])
        self.run_command([self.pip, 'install', core_targz],
                         shell=False)
        self._del_core_noneed_file()
        _print_message("Setup core package install success.")

    def _update_pip(self):
        self.run_command([self.pip, 'install', '--upgrade', 'pip'],
                         shell=False)
        _print_message('.Venv pip update ok.')

    def _pip_install_package(self, package):
        self.run_command([self.pip, 'install', package],
                         shell=False)
        _print_message('Pip install %s ok.' % package)

    def install_dependencies(self):
        self._update_pip()
        self._pip_install_package('setuptools')
        self._pip_install_package('pbr')
        self._pip_install_requirements()
        # self._pip_install_core()


def _get_cur_folder():
    """
    get current folder, solve is or not frozen of the script
    :return: 
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(cur_folder)


def _print_message(message, t="default"):
    """
    print message by message level
    default 
    important = = = = =
    error * * * * * * *
    :param message: 
    :param t: 
    :return: 
    """
    if t == 'error':
        print("%s\n%s\n%s" % ("* " * 20, message, "* " * 20))
    elif t == 'important':
        print("%s\n%s\n%s" % ("= " * 20, message, "= " * 20))
    else:
        print(message)


def main():
    py_version = python_version()
    if py_version < MAX_PYTHON_VERSION:
        _print_message("Current is low, please use Python3.X.X", t="error")
        os._exit(0)

    base_dir = _get_cur_folder()
    venv = os.path.join(base_dir, '.venv')
    if os.environ.get('.venv'):
        venv = os.environ.get('.venv')
    pip_requirements = os.path.join(base_dir, 'requirements.txt')
    setup = os.path.join(base_dir, 'setup.py')

    install = InstallEnv(base_dir, venv, setup, pip_requirements, py_version)
    install.check_or_create_virtualenv()
    if not install.check_venv():
        install.install_venv()
    install.activate_venv_p()
    install.install_dependencies()
    install.print_help(venv, py_version)


if __name__ == '__main__':
    main()
