# Usage: sudo python3 wg_watcher.py
import logging.config
import time
import os
import argparse
import subprocess
from demon import Daemon
from settings import LogConfig


def wg_stop(wg_port, wg_filename, wg_interface):
    logging.info(f'Port {wg_port} is found')
    logging.info('Attempt to stop wg...')
    try:
        code_return = subprocess.check_call(['wg-quick', 'down', wg_interface])
        logging.info(f'Code return: {code_return}')
    except:
        logging.error('Failed to stop wg')

    d = Daemon(wg_filename)
    d.stop()


def wg_restart(*args):
    port, filename, interface = args
    wg_stop(port, filename, interface)
    d = Daemon(filename)
    d.start(watcher, wg_args.port, wg_args.interface)


def watcher(*args):
    wg_port, wg_interface = args
    udp_file = '/proc/net/udp'
    logging.debug('Start watcher!')

    while True:
        ports = []
        with open(udp_file) as f:
            open_udp = f.readlines()

        for prog_list in open_udp[1:]:
            try:
                prog_split = prog_list.split(':')
                raw_port = prog_split[2].split()[0]
                ports.append(int(raw_port, 16))
                logging.debug(ports)
            except IndexError as ie:
                logging.error(ie)

        if int(wg_port) in ports:
            logging.info(f'Port {wg_port} is found')
            time.sleep(3600)
            continue
        else:
            logging.info(f'Port {wg_port} not found')
            logging.info('Attempt to run wg...')
            code_return = subprocess.check_call(['wg-quick', 'up', wg_interface])
            logging.info(f'Code return: {code_return}')




parser = argparse.ArgumentParser()
parser.description = 'It is the simple watchdog for start up and checking WireGuard interface'
parser.epilog = 'Example of launch with the DEBUG level verbosity: python3 wg_watcher.py -i wg0 -vv'
parser.add_argument('-p', '--port', action='store', default='62931', help='Enter a WierGuard port')
parser.add_argument('-i', '--interface', action='store', default='wg0', help='Enter either name or path to config WireGuard interface')
parser.add_argument('-f', '--filename', action='store', default='watcher', help='Enter the name for lock and config files. Default: watcher.log && /var/lock/watcherd')
parser.add_argument('-v', '--verbose', action='count', default=2, help='Choose loglevel verbosity. Default: WARNING')

exgroup = parser.add_mutually_exclusive_group()
exgroup.add_argument('-s', '--stop', action='store_true', help='Stop a dogwatcher and down the interface')
exgroup.add_argument('-r', '--restart', action='store_true', help='Restart WireGuard watcher')
wg_args = parser.parse_args()


if __name__ == '__main__':
    if not os.getegid():
        FORMAT = '%(asctime)s::%(name)s::%(levelname)s::%(message)s'
        loglevel = 50 - wg_args.verbose * 10
        LogConfig['handlers']['rotate']['filename'] = f'{wg_args.filename}.log'

        logging.config.dictConfig(LogConfig)
        logging.getLogger().level = loglevel

        logging.debug(wg_args)

        if wg_args.stop:
            wg_stop(wg_args.port, wg_args.filename, wg_args.interface)

        elif wg_args.restart:
            wg_restart(wg_args.port, wg_args.filename, wg_args.interface)

        else:
            logging.debug('Attempt start and create demon...')
            d = Daemon(wg_args.filename)
            d.stdout = d.stderr = f'{wg_args.filename}.log'
            d.start(watcher, wg_args.port, wg_args.interface)

    else:
        print('Get running with sudo!')
