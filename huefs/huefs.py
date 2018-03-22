import logging
from configparser import ConfigParser
from pathlib import Path
from sys import argv

import phue

import requests
from fuse import Operations, LoggingMixIn, FUSE


class HueBridge:
    def __init__(self):
        self.bridge_ip = self.locate_bridge()

    def locate_bridge(self):
        return requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']

    def new_user(self):
        result = requests.post('http://{}/api'.format(self.bridge_ip), json={'devicetype':'huefs'}).json()
        return result[0]['success']['username']

class ConfiguredBridge:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(Path.home() / '.config/huefs/huefs.ini')

        self.active_bridge = self.config['defaults']['bridge']
        self.internalipaddress = self.config[self.active_bridge]['internalipaddress']
        self.username = self.config[self.active_bridge]['username']

    def lights(self):
        return requests.get('http://{}/api/{}/lights'.format(self.internalipaddress, self.username)).json()

    def switch(self, light, on):
        requests.put('http://{}/api/{}/lights/{}/state'.format(self.internalipaddress, self.username, light), json={'on':on})




class HueFilesystem(LoggingMixIn, Operations):
    def __init__(self, bridge):
        self.bridge = bridge

    def readdir(self, path, fh):
        if path == '/':
            return ['.', '..'] + [x.name for x in self.bridge.lights]


def main():
    logging.basicConfig(level=logging.DEBUG)
    cb = ConfiguredBridge()
    bridge = phue.Bridge(cb.internalipaddress, cb.username)
    fuse = FUSE(HueFilesystem(bridge), argv[1], foreground=True, ro=True)