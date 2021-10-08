import requests
from urllib3.exceptions import InsecureRequestWarning
import yaml
import json


class d42api ():
    def __init__(self, config_path):
        self.config = self._import_config(path=config_path)
        requests.packages.urllib3.disable_warnings(
            category=InsecureRequestWarning)

    def _import_config(self, path):
        try:
            with open(path, "r") as stream:
                try:
                    cfg = yaml.safe_load(stream)
                    return cfg
                except yaml.YAMLError as exc:
                    print(exc)
                    return None
        except IOError as exc:
            print(exc)
            return None

    def lookup_enduser(self, id):
        print("Querying Device42 for End User matching ID: " + id + " ...")
        data = {"output_type": "json",
                "query": "select name from view_enduser_v1 where enduser_pk = " + id}
        response = requests.post(self.config['host'] + "/services/data/v1.0/query/",
                                 auth=(self.config['username'], self.config['password']), data=data, verify=self.config['verify'])
        if(response.json()):
            print("Response: '" + response.json()[0]['name'] + "'\n")
            return response.json()[0]
        else:
            print("No match found\n")
            return None

    def lookup_device(self, id):
        print("Querying Device42 for Device matching ID: " + id + " ...")
        data = {"output_type": "json",
                "query": "select name from view_device_v2 where device_pk = " + id}
        response = requests.post(self.config['host'] + "/services/data/v1.0/query/",
                                 auth=(self.config['username'], self.config['password']), data=data, verify=self.config['verify'])
        if(response.json()):
            print("Response: '" + response.json()[0]['name'] + "'\n")
            return response.json()[0]
        else:
            print("No match found\n")
            return None

    def lookup_asset(self, id):
        print("Querying Device42 for Asset matching ID: " + id + " ...")
        data = {"output_type": "json",
                "query": "select name from view_asset_v1 where asset_pk = " + id}
        response = requests.post(self.config['host'] + "/services/data/v1.0/query/",
                                 auth=(self.config['username'], self.config['password']), data=data, verify=self.config['verify'])

        if(response.json()):
            print("Response: '" + response.json()[0]['name'] + "'\n")
            return response.json()[0]
        else:
            print("No match found\n")
            return None

    def update_device_cf(self, name, key, value):
        print("Updating Device Custom Field: '" + key +
              "' on device: '" + name + "' with value: '" + value + "'")
        data = {
            'name': name,
            'key': key,
            'value': value
        }
        response = requests.put(self.config['host'] + '/api/1.0/device/custom_field/',
                                auth=(self.config['username'], self.config['password']), data=data, verify=self.config['verify'])
        if(response.json()):
            print("Response: '" + response.json()['msg'][0] + "'\n")

    def update_asset_cf(self, name, key, value):
        print("Updating Asset Custom Field: '" + key +
              "' on asset: '" + name + "' with value: '" + value + "'")
        data = {
            'name': name,
            'key': key,
            'value': value
        }
        response = requests.put(self.config['host'] + '/api/1.0/custom_fields/asset/',
                                auth=(self.config['username'], self.config['password']), data=data, verify=self.config['verify'])
        if(response.json()):
            print("Response: '" + response.json()['msg'][0] + "'\n")
