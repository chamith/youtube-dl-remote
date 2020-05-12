#! /usr/bin/python3

import requests
import getopt
import sys
#ARGS = "-h -p "

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5000

opts, args = getopt.getopt(sys.argv[1:],"h:p:v", ["host=","port="])

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
    print("###### Request Queue ######")
    print()
    for data in resp.json():
        print('{}'.format(data['url']))
        items = data['items']
        for item in items:
            print('|-[{}] {}'.format(get_status_text_short(item['status']), item['title']))
        print()

def cmd_add(url, schedule=0):
    payload = {'url': url, 'schedule': schedule}
    resp = requests.post('http://{}:{}/api/requests'.format(host, port), json=payload)

    if resp.status_code != 201:
        print("Error posting the request")
        print(resp.reason)
        exit(-1)
        # This means something went wrong.
    
    print("Url \'{}\' added to the queue successfully.".format(url))

def cmd_help():
    print('Usage:\t{} [options] <command> <arg1> <arg2>'.format(sys.argv[0]))
    print('Commands:\n\
        ls  \tshows the queue\n\
        add \tadds a url to the queue')
    print('Options:\n\
        -h  --host [default: {}]\n\
        -p  --port [default: {}]'.format(DEFAULT_HOST, DEFAULT_PORT))

host = get_opt_val(opts, '-h', DEFAULT_HOST)
port = get_opt_val(opts, '-p', DEFAULT_PORT)

if len(args) == 0:
    cmd_help()
    exit(0)

if args[0] == 'ls':
    cmd_ls()
elif args[0] == 'add':
    cmd_add(args[1])
else:
    print('no command provided')