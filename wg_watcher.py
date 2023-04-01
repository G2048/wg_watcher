import logging
import time
import os
import subprocess
import sys


FORMAT = '%(asctime)s::%(levelname)s::%(message)s'
logging.basicConfig(filename='wg.log', filemode='w', format=FORMAT, level=logging.DEBUG)


def demonification(fn):
    def wrap(*args):
        pid = os.fork()
        logging.info(f'Pid is: {pid}')

        if not pid:
            logging.debug('Demon was created')
            fn()
        else:
            logging.info('Exit!')
            sys.exit(0)
    return wrap


@demonification
def watcher():
    udp_file = '/proc/net/udp'

    while True:
        ports = []
        with open(udp_file) as f:
            open_udp = f.readlines()

        for prog_list in open_udp:
            try:
                prog_split = prog_list.split(':')
                raw_port = prog_split[2].split()[0]
                ports.append(int(raw_port, 16))
            except IndexError:
                pass

        if 62931 in ports:
            logging.info('Port 62931 is found')
            time.sleep(3600)
            continue
        else:
            logging.info('Port 62931 not found')
            logging.info('Attempt to run wg...')
            code_return = subprocess.check_call(['wg-quick', 'up', 'wg0'])
            logging.info(f'Code return: {code_return}')


if __name__ == '__main__':
    if not os.getegid():
        watcher()
    else:
        print('Get running with sudo!')
