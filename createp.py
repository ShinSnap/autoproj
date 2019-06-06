#!/usr/bin/env python3
import os, requests, json, sys

# Set Variables
projectname = sys.argv[1]
authorization_token = os.environ.get('GITHUBAPI')

def createprojectfolder(projectname):
    home = os.path.expanduser('~')
    workdir = home + '/git/Personal/' + projectname
    os.mkdir(workdir)
    os.chdir(workdir)


def createreadme():
    open('README.md', 'a').close()


def initializegit():
    os.system('git init')
    os.system('git add README.md')
    os.system('git commit -m "initial commit"')


def githubremote(githuburl):
    os.system('git remote add origin ' + githuburl)


def githubpush():
    os.system('git push -u origin master')


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

    response = requests.post(uri, params=json.dumps(parameters), headers=header)
    if response.status_code == 201:
        print('Successfully created Repo')
        data = json.loads(response.content)
        return data['ssh_url']
    else:
        print('...Error creating repo...')
        exit()


def openvscode():
    os.system('code .')


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
