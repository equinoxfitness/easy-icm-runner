"""
the following is a simple hand dispatched integration test, better testing to come!
customize and rename SAMPLE_test.cfg with your own configurations
"""

import configparser
from icm_runner import exec_runner

config = configparser.ConfigParser()
config.read('test.cfg')

username = config.get('test', 'username')
password = config.get('test', 'password')
model_name = config.get('test', 'model_name')
process_name = config.get('test', 'process_name')
api_key = config.get('test', 'api_key')

print("---first executing via api_key---")
exec_runner(username=username,  model_name=model_name,
            process_name=process_name, api_key=api_key)
print("---now executing via username, pwd---")
exec_runner(username=username, password=password, model_name=model_name,
            process_name=process_name)

