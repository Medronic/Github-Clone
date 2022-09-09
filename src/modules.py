import sys
from subprocess import call
import json
import os
import datetime

import requests

# DEFINES

LOAD_SETTINGS = "Loading settings..."
LOAD_SETTINGS_SUCCESS = "Settings loaded successfully!"
LOAD_SETTINGS_ERROR = "Error loading settings!"

SAVE_SETTINGS = "Saving settings..."
SAVE_SETTINGS_SUCCESS = "Settings saved successfully!"
SAVE_SETTINGS_ERROR = "Error saving settings!"

# Função para Salvar arquivos de Log

def SaveLogs(p1):
    with open('logs.txt', 'a', encoding='utf-8') as outfile:
        date = datetime.datetime.now()
        outfile.write(f"{date} - {p1}")

# Função para salvar as configurações

def SaveSettings(p1 = None, p2 = None, p3 = None, p4 = None, p5 = None, p6 = None):
    data = {}
    data['Settings'] = {'Application': {'Name': AppName, 'Description': AppDescription, 'Author': AppAuthor, 'AuthorNickname': AppAuthorNickname, 'Version': AppVersion}, 'UI': {'Theme': p1, 'Language': p2, 'DownloadPath': p3}}
    with open('settings.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)

# Função para Ler as Configurações do Arquivo JSON

def LoadSettings():
    SaveLogs(f"Loading settings...\n")

    msgLog = None

    if os.path.isfile('settings.json'):
        arquivo_json = open('settings.json', 'r', encoding='utf-8')
        data = json.loads(arquivo_json.read())

        # Variáveis Globais da Aplicação
        
        global AppName
        global AppDescription
        global AppAuthor
        global AppAuthorNickname
        global AppVersion

        global stgTheme
        global stgLang
        global stgDownloadPath

        # Configurações da Aplicação

        AppName = data['Settings']['Application']['Name']
        AppDescription = data['Settings']['Application']['Description']
        AppAuthor = data['Settings']['Application']['Author']
        AppAuthorNickname = data['Settings']['Application']['AuthorNickname']
        AppVersion = data['Settings']['Application']['Version']

        stgTheme = data['Settings']['UI']['Theme']
        stgLang = data['Settings']['UI']['Language']
        stgDownloadPath = data['Settings']['UI']['DownloadPath']

        SaveLogs(f"Settings loaded successfully!\n")
    else:
        SaveLogs("Settings file not found! Creating default settings file...\n")
        
    SaveLogs(f"Loading Languages...\n")

    if os.path.isfile('languages.json'):
        arquivo_json = open('languages.json', 'r', encoding='utf-8')
        data = json.loads(arquivo_json.read())

        # Variáveis Globais do Idioma
        
        global lngLblUser
        global lngLblDir
        global lngBtnDownloadRepositories

        global lngStatusMsg1
        global lngStatusMsg2
        global lngStatusMsg3
        global lngStatusMsg4
        global lngStatusMsg5
        global lngStatusMsg6
        global lngStatusMsg7

        global lngStatusPath1

        global lngLblTheme

        # Variáveis Globais de Configurações da Aplicação

        lngLblUser = data[f'{stgLang}'][0]['lblUser']
        lngLblDir = data[f'{stgLang}'][0]['lblDir']
        lngBtnDownloadRepositories = data[f'{stgLang}'][0]['btnDownloadRepositories']
        lngStatusMsg1 = data[f'{stgLang}'][0]['lblStatusMsg1']
        lngStatusMsg2 = data[f'{stgLang}'][0]['lblStatusMsg2']
        lngStatusMsg3 = data[f'{stgLang}'][0]['lblStatusMsg3']
        lngStatusMsg4 = data[f'{stgLang}'][0]['lblStatusMsg4']
        lngStatusMsg5 = data[f'{stgLang}'][0]['lblStatusMsg5']
        lngStatusMsg6 = data[f'{stgLang}'][0]['lblStatusMsg6']
        lngStatusMsg7 = data[f'{stgLang}'][0]['lblStatusMsg7']
        lngStatusPath1 = data[f'{stgLang}'][0]['lblStatusPath1']

        lngLblTheme = data[f'{stgLang}'][0]['lblTheme']

        msgLog = f"Language Settings successfully loaded!\n"
        SaveLogs(msgLog)
    else:
        SaveLogs(f"Language file settings not found! Creating default language file...\n")

# Função para pegar a pasta de Downloads do usuário

def GetDownloadPath():
    if os.name == 'posix':
        return os.path.expanduser('~/Downloads')
    elif os.name == 'nt':
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        return os.getcwd()

# Função para verificar se o diretório existe

def VerifyPath(path):
    if os.path.isdir(path):
        return True
    else:
        return False

# Função para baixar os repositórios
def DownloadRepositories(user, path):
    global status

    url = 'https://api.github.com/users/{0}/repos'.format(user)
    error = False
    status = f"No errors for now!"

    try:
        r = requests.get(url, timeout=10)

    except requests.Timeout as e:
        status = f'{lngStatusMsg3}'
        SaveLogs(status)
        return status
        error = True
    except requests.ConnectionError as e:
        status = f'{lngStatusMsg4}'
        SaveLogs(status)
        return status
        error = True
    except socket.error as e:
        status = f'{lngStatusMsg5}'
        SaveLogs(status)
        return status
        error = True
    except exception as e:
        status = e.message
        SaveLogs(e.message)
        return status
        error = True

    if (error == True):
        status = f'{lngStatusMsg6}'
        SaveLogs(e.message)
        return status
        # exit(1)

    if (r.status_code == 404):
        status = f'{lngStatusMsg7}'
        return status
        # exit(1)

    json_data = r.text

    data = json.loads(json_data)

    os.chdir(path)

    status = 'Downloading repositories...'
    SaveLogs(status)

    for i in range(0, len(data)):
        print('Cloning %i / %i' % (i+1, len(data)))
        print('Cloning repository: %s' % data[i]['name'])

        call(['git', 'clone', data[i]['clone_url']])
        status = 'All repositories cloned successfully!'