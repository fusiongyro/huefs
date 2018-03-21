import os.path
from configparser import ConfigParser
from pathlib import Path

import requests

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