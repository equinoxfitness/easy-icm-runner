from pprint import pprint
from icm_runner import Runner

job_runner = Runner()

job_runner.get_token(username='xxx', password='xxx')
activity_id = job_runner.run_process_by_name(model_name='xxx', process_name='xxx')

job_runner.monitor_activity(model_name='EquinoxDev', activity_id=activity_id, interval_mins=0.1)