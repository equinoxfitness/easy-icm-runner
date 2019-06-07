from pprint import pprint
from icm_api import Runner

job_runner = Runner()

job_runner.get_token(username='zzz', password='zzz')
resp = job_runner.run_process_by_name(model_name='EquinoxDev', process_name='Test',follow=True)
print(resp["value"])
# job_runner.monitor_activity(model_name='EquinoxDev', activity_id=resp["value"], interval_mins=0.1)
