from os.path import exists
from rich.console import Console
import configparser
console = Console()
cfg = configparser.ConfigParser()
cfg.read('config.cfg')

if not exists("./config.cfg"):
    ftext=console.input("[bold white]Type your api_id: ")
    cfg.add_section('session')
    cfg.set('session', 'api_id', ftext)
    fstext=console.input("[bold white]Type your api_hash: ")
    cfg.set('session', 'api_hash', fstext)
    cfg.add_section('settings')
    cfg.set('settings', 'dict', 'none')
    cfg.set('settings', 'delay', '2')
    cfg.set('settings', 'prefix', '/')
    with open('config.cfg', 'w') as configfile:
        cfg.write(configfile)

api_id = cfg.get('session', 'api_id')
api_hash = cfg.get('session', 'api_hash')
