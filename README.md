# easy-icm-runner :rocket:
Simplified Job Execution for Varicent's ICM v10 using REST APIs

## Installation:
```
pip install easy-icm-runner
```

## Usage:
This project can be used as a module within your custom program, or standalone from the command line.  Below we demonstrate sample usage:

### Python

The snippet below demonstrates running a job _syncronously_ in python code.  Such a method will be desirable for incorporating an ICM job step into a more complex application, or such tasks as integrating your own secret and configuration management.
```python
from icm_runner import Runner

job_runner = Runner()

# get an authentication token to use in remaining operations
job_runner.get_token(username='icm username', password='icm password')
# start job
activity_id = job_runner.run_process_by_name(model_name='model name', process_name='process name', follow=True)
# poll for status until complete
job_runner.monitor_activity(model_name='model name', activity_id=activity_id, interval_mins=0.1)

```

### Command Line
For those of you who are not budding pythonistas, or just looking for a simple solution to job scheduling we also allow a command line entrypoint.   
```text
$ python -m icm_runner -u "icm username" -p "icm password" -m "model name" -j "process name"
```
