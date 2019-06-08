# easy-icm-runner :rocket:
Simplified Job Execution for IBM ICM v10 using REST APIs

https://developer.ibm.com/api/view/id-689:title-Incentive_Compensation_Management

## Usage:
This project can be used as a module within your custom program, or standalone from the command line.  Below we demonstrate sample usage:

### Python

The snippet below demonstrates running a job _syncronously_ in python code.  Such a method will be desirable for secret and configuration management, or for integrating into a more complex application.
```python
from icm_runner import Runner

job_runner = Runner()

job_runner.get_token(username='icm username', password='icm password')
job_runner.run_process_by_name(model_name='model name', process_name='process name',follow=True)
```

### Command Line
For those of you who are not budding pythonistas, or just looking for a simple solution to job scheduling we also allow a command line entrypoint.   
```text
$ python icm_runner.py -u "icm username" -p "icm password" -m "model name" -j "process name"
```
