# The WireGuard Watcher

![Wireguard](https://www.wireguard.com/img/wireguard.svg)
More about [WireGuard](https://www.wireguard.com/quickstart/)

## Overview

It is a simple daemon-watcher for WireGuard.

## Documentation

### QuickStart
You should download the project:
```
git clone https://github.com/G2048/wg_watcher.git
```

Get start the deamon of wg_watcher:
```zsh
sudo python3 wg_watcher.py -vv 
```

*P.S. log file by default is watcher.log , If you want to change it use -f option*

### Usage
```python
usage: wg_watcher.py [-h] [-p PORT] [-i INTERFACE] [-f FILENAME] [-v] [-s | -r]

It is the simple watchdog for start up and checking WireGuard interface

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Enter a WierGuard port
  -i INTERFACE, --interface INTERFACE
                        Enter either name or path to config WireGuard interface
  -f FILENAME, --filename FILENAME
                        Enter the name for lock and config files. Default: watcher.log && /var/lock/watcherd
  -v, --verbose         Choose loglevel verbosity. Default: WARNING
  -s, --stop            Stop a dogwatcher and down the interface
  -r, --restart         Restart WireGuard watcher

Example of launch with the DEBUG level verbosity: python3 wg_watcher.py -i wg0 -vv
```

>For more details about WireGuard see [WireGuard QuickStart Guide](https://www.wireguard.com/quickstart/)

