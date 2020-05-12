#! /usr/bin/python3

import requests
import getopt
import sys
import os.path
from pathlib import Path
#ARGS = "-h -p "
USER_HOME_DIR = str(Path.home())
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5000
CONFIG_FILE = USER_HOME_DIR + '/.youtube-dl-remote/settings.conf'


def get_config_settings():
    config_settings = {}

    if not os.path.isfile(CONFIG_FILE):
        return config_settings

    with open(CONFIG_FILE) as f_in:
        lines = filter(None, ((not line.startswith('#') and line.rstrip()) for line in f_in))

        for line in lines:
            line = line.split('=')
            config_settings[line[0]] = line[1]

    return config_settings


def get_opt_val(opts, key, default_value):
    for opt in opts:
        if opt[0] == key:
            return opt[1]
    return default_value


def get_status_text(code):
    if code == 0:
        return 'pending'
    elif code == 1:
        return 'in-progress'
    elif code == 2:
        return 'paused'
    elif code == 3:
        return 'completed'
    elif code == -1:
        return 'error'
    else:
        return 'unknown'


def get_status_text_short(code):
    if code == 0:
        return 'P'
    elif code == 1:
        return 'I'
    elif code == 2:
        return 'H'
    elif code == 3:
        return 'C'
    elif code == -1:
        return 'E'
    return 'U'


def get_schedule_text(code):
    if code == 0:
        return 'off-peak-only'
    if code == 1:
        return 'anytime'
    return 'unknown'


def get_schedule_text_short(code):
    if code == 0:
        return 'O'
    if code == 1:
        return 'A'
    return 'U'


def cmd_ls(status=3, schedule=1):
    resp = requests.get('http://{}:{}/api/requests'.format(host, port))
    if resp.status_code != 200:
        print("Error connecting to the server")
        exit(-1)
        # This means something went wrong.
        #raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    print()
    print("###### Request Queue on {}:{} ######".format(host, port))
    print()
    for data in resp.json():
        print('{} - {}'.format(data['id'], data['url']))
        items = data['items']
        for item in items:
            print(
                '|-[{}] {}'.format(get_status_text_short(item['status']), item['title']))
        print()

def cmd_rm(id):
    resp = requests.delete('http://{}:{}/api/requests/{}'.format(host, port, id))
    if resp.status_code != 200:
        print("Error posting the request")
        exit(-1)
    
    print("Request with id \'{}\' has been removed successfully.".format(id))

def cmd_add(url, schedule=0):
    payload = {'url': url, 'schedule': schedule}
    resp = requests.post(
        'http://{}:{}/api/requests'.format(host, port), json=payload)

    if resp.status_code != 201:
        print("Error posting the request")
        print(resp.reason)
        exit(-1)
        # This means something went wrong.

    print("Url \'{}\' added to the queue successfully.".format(url))


def cmd_help():
    print('Usage:\t{} [options] <command> <arg1> [<arg2>]'.format(sys.argv[0]))
    print('Commands:\n\
        ls  \tshows the queue\n\
        add \tadds a url to the queue')
    print('Options:\n\
        -h  --host [default: {}]\n\
        -p  --port [default: {}]'.format(DEFAULT_HOST, DEFAULT_PORT))


def cmd_info():
    print('Host: {}'.format(host))
    print('Port: {}'.format(port))


opts, args = getopt.getopt(sys.argv[1:], "h:p:v", ["host=", "port="])

configs = get_config_settings()

# print('host:{}'.format(configs['host']))

host = get_opt_val(opts, '-h', configs.get('host', DEFAULT_HOST))
port = get_opt_val(opts, '-p', configs.get('port', DEFAULT_PORT))

if len(args) == 0:
    cmd_help()
    exit(0)

if args[0] == 'ls':
    cmd_ls()
elif args[0] == 'add':
    if len(args) == 2:
        cmd_add(args[1])
    else:
        cmd_add(args[1], args[2])
elif args[0] == 'rm':
    cmd_rm(args[1])
elif args[0] == "info":
    cmd_info()
else:
    print('no command provided')
