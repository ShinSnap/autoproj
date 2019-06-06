#!/usr/bin/env python3
import requests
import json
from sys import argv
from platform import mac_ver
from os import environ, path, mkdir, chdir, system

# Set Variables
projectname = argv[1]
authorization_token = environ.get('GITHUBAPI')


def createprojectfolder(projectname):
    home = path.expanduser('~')
    workdir = home + '/git/Personal/' + projectname
    mkdir(workdir)
    chdir(workdir)


def createreadme():
    open('README.md', 'a').close()


def initializegit():
    system('git init')
    system('git add README.md')
    system('git commit -m "initial commit"')


def githubremote(githuburl):
    system('git remote add origin ' + githuburl)


def githubpush():
    system('git push -u origin master')


def githubapi(projectname, authorization_token):

    uri = 'https://api.github.com/user/repos'

    header = {
        'Authorization': 'token ' + authorization_token,
    }
    parameters = {
        'name': projectname,
        'private': True,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }

    response = requests.post(
        uri,
        params=json.dumps(parameters),
        headers=header
    )
    if response.status_code == 201:
        print('Successfully created Repo')
        data = json.loads(response.content)
        return data['ssh_url']
    else:
        print('...Error creating repo...')
        exit()


def openvscode():
    system('code .')


def checkos():
    os = mac_ver()[0]
    if os:
        return True
    else:
        print('This script is only meant for macOS')
        exit()


if checkos() is True:
    try:
        createprojectfolder(projectname)
        createreadme()
        initializegit()
        repourl = githubapi(projectname, authorization_token)
        githubremote(repourl)
        githubpush()
        openvscode()
    except FileExistsError:
        print('Project exists. Choose another name.')
        exit()
else:
    print('Error running script')
