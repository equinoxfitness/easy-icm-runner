from pprint import pprint
from icm_runner import Runner

job_runner = Runner()

job_runner.get_token(username='xxx', password='xxx')
resp = job_runner.run_process_by_name(model_name='xxx', process_name='Test',follow=True)

# job_runner.monitor_activity(model_name='EquinoxDev', activity_id=resp["value"], interval_mins=0.1)