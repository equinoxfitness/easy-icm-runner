'''
the following is a simple hand dispatched integration test, better testing to come
'''
import configparser
from icm_runner import Runner

config = configparser.ConfigParser()
config.read('test.cfg')

username = config.get('test', 'username')
password = config.get('test', 'password')
model_name = config.get('test', 'model_name')
process_name = config.get('test', 'process_name')


job_runner = Runner()

job_runner.get_token(username=username, password=password)
activity_id = job_runner.run_process_by_name(model_name=model_name, process_name=process_name)

job_runner.monitor_activity(model_name=model_name, activity_id=activity_id, interval_mins=0.1)