import json
from flask import Flask, request
from datetime import datetime
from d42.d42 import d42api

app = Flask(__name__)
config_path = '../config.yaml'

d42_api = d42api(config_path)


@app.route('/', methods=['POST'])
def foo():
    hook = request.json

    print("\nRecieved webhook: " + datetime.now().strftime("%d-%b-%Y (%H:%M:%S)") +
          "\nWebhook Body: \n" + json.dumps(hook, indent=2) + "\n")

    # Check to see if the webhook category is a asset lifecycle event
    if(hook['category'] == 'asset_lifecycle'):
        # Check to see if the asset life cycle event is of type 'Assigned'
        if(hook['data']['type_id'] == '7'):
            # Check to see if a End User was specified
            if(hook['data']['user_id']):
                if(hook['data']['device_id'] or hook['data']['asset_id']):
                    subject = {}
                    print(["1/3"])
                    if(hook['data']['device_id']):
                        subject = {
                            'data': d42_api.lookup_device(
                                hook['data']['device_id']),
                            'type': 'device'
                        }
                    elif(hook['data']['asset_id']):
                        subject = {
                            'data': d42_api.lookup_asset(
                                hook['data']['asset_id']),
                            'type': 'asset'
                        }
                    if(subject['data']):
                        print(["2/3"])
                        end_user = d42_api.lookup_enduser(
                            hook['data']['user_id'])

                        if(end_user):
                            print(["3/3"])
                            if(subject['type'] == 'asset'):
                                d42_api.update_asset_cf(name=subject['data']['name'],
                                                        key='Assigned', value=end_user['name'])
                            elif(subject['type'] == 'device'):
                                d42_api.update_device_cf(name=subject['data']['name'],
                                                         key='Assigned', value=end_user['name'])
                else:
                    print("No Device/Asset ID found in hook\n")
            else:
                print("No End User ID found in hook\n")

    return "OK"


if __name__ == '__main__':
    app.run()
