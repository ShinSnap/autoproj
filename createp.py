#!/usr/bin/env python3
import requests
from sys import argv
from platform import mac_ver
from os import environ, path, mkdir, chdir, system

# Set Variables
authorization_token = environ.get('GITHUBAPI')


class GitHub:

    def __init__(self, authorization_token, project_name=None):
        self._URI = 'https://api.github.com/user/repos'
        self._token = authorization_token
        self._project_name = project_name

    def create_repo(self, private=False, issues=True, projects=True,
                    wiki=True, license_template='mit'):

        header = {
            'Authorization': 'token ' + self._token,
        }
        parameters = {
            'name': self._project_name,
            'private': private,
            'has_issues': issues,
            'has_projects': projects,
            'has_wiki': wiki,
            'license_template': license_template,
            'auto_init': True
        }

        response = requests.post(
            self._URI,
            headers=header,
            json=parameters
        )

        if response.status_code == 201:
            print('Repo Created')
            data = response.json()['ssh_url']
            return data
        else:
            print('...Error creating repo...')
            print(response.content)
            exit()


def createprojectfolder(projectname):
    home = path.expanduser('~')
    workdir = home + '/git/dev/' + projectname
    mkdir(workdir)
    chdir(workdir)


def initializegit():
    system('git init')
    system('git commit -m "initial commit"')


def createreadme():
    open('README.md', 'a').close()


def checkos():
    os = mac_ver()[0]
    if os:
        return True
    else:
        print('This script is only meant for macOS')
        exit()


if __name__ == '__main__':
    if checkos() is True:
        try:
            projectname = argv[1]
            createprojectfolder(projectname)
            initializegit()
            github = GitHub(authorization_token, projectname)
            repourl = github.create_repo(private=True)
            system('git remote add origin {}'.format(repourl))
            system('git pull origin master')
            system('code .')
        except FileExistsError:
            print('Project exists. Choose another name.')
            exit()
        except IndexError:
            print('Please state project name when executing command')
            print('Usage: create <projectname>')
            print('Example: create HelloWorld')
            exit()
    else:
        print('Error running script')
