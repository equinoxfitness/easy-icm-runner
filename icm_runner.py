"""
IBM ICM API Calls Classes
Complete list: https://developer.ibm.com/api/view/id-689:title-Incentive_Compensation_Management
"""

import time
import logging as log
import argparse
import requests

log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)

SPM_URL = 'https://spm.ibmcloud.com'

PARSER = argparse.ArgumentParser()

class Runner:
    """
    The main class that contains the required ICM API Call
    Functions to manage running the Scheduler
    """
    def __init__(self, api_key=None):
        """
        Intializes a class
        """
        self.login_url = f"{SPM_URL}/services/login"
        self.token = ""
        if api_key:
            self.token = api_key

    def get_token(self, username, password):
        """
        Gets the token needed for making api calls
        :param username:
        :param password:
        :return:
        """
        log.info("Getting token for %s", username)
        call_data = {
            "email": username,
            "password": password,
            "content-type": "application/json"
        }
        req = requests.post(url=self.login_url, data=call_data)
        req_obj = req.json()
        if req.status_code == 200:
            log.info("Token obtained successfuly")
            self.token = req_obj["token"]
        else:
            msg = req_obj["message"]
            raise Exception(f"{req.status_code}. Issue getting token: {msg}")

    def build_header(self, model_name):
        """
        builds standard header
        :param model_name:
        :return:
        """
        header = {
            "authorization": "bearer " + self.token,
            "model": model_name,
            "content-type": "application/json"
        }
        return header

    def get_process_id(self, model_name, process_name):
        """
        Gets the top level process id using a given process name
        :param model_name:
        :param process_name:
        :return: process_id
        """
        url = f"{SPM_URL}/api/v1/scheduleitem"
        process_id = -1
        header = self.build_header(model_name=model_name)
        req = requests.get(url=url, headers=header)
        req_obj = req.json()
        if req.status_code != 200:
            msg = req_obj["Message"]
            raise Exception(f"{req.status_code}. Issue getting process id: {msg}")

        for i in req.json():
            if i["name"] == process_name:
                process_id = str(i["id"])
                log.info("Process id = %s", process_id)
                break

        if process_id == -1:
            raise Exception("Invalid process name specified")

        return process_id

    def run_process_by_id(self, model_name, process_id):
        """
        Runs a process by its id
        :param model_name:
        :param process_id:
        :param follow:
        :return: activity_id
        """
        url = f"{SPM_URL}/api/v1/rpc/scheduleitem/{process_id}/run"
        header = self.build_header(model_name=model_name)
        req = requests.post(url=url, headers=header)
        req_obj = req.json()
        if req.status_code == 200:
            log.info("Process run scheduled (immediate) successfully")
            activity = req_obj["liveactivities"]
            pos = len(activity) - activity.rfind("/", 1, 9999) - 1
            activity_id = activity[-pos:]
        else:
            msg = req_obj["Message"]
            raise Exception(f"{req.status_code}. Issue scheduling process: {msg}")
        log.info("Activity id = %s", activity_id)
        return activity_id

    def run_process_by_name(self, model_name, process_name):
        """
        Runs a top level process by its name
        """
        process_id = self.get_process_id(model_name, process_name)
        activity_id = self.run_process_by_id(model_name=model_name, process_id=process_id)
        return activity_id

    def get_live_activity_status(self, model_name, activity_id):
        """
        Gets the status of a live activity by its id
        :param model_name:
        :param activity_id:
        :return: res
        """
        url = f"{SPM_URL}/api/v1/liveactivities?liveActivityDTO={activity_id}"
        headers = self.build_header(model_name=model_name)
        res = {}
        req = requests.get(url=url, headers=headers)
        req_obj = req.json()
        if req.status_code != 200:
            msg = req_obj["Message"]
            raise Exception(f"{req.status_code}. Issue getting activity status: {msg}")

        if req.status_code == 200:
            for dic in req_obj:
                if "type" in dic.keys():
                    res["message"] = dic["status"]
                    res["value"] = dic["percent"]
                    break

        if not res:
            res = self.get_completed_activity_status(model_name=model_name, activity_id=activity_id)

        return res

    def get_all_completed_activities(self, model_name):
        """
        Gets a list of all the completed activities
        :param model_name:
        :return:
        """
        url = f"{SPM_URL}/api/v1/completedactivities"
        header = self.build_header(model_name=model_name)
        req = requests.get(url=url, headers=header)
        req_obj = req.json()
        if req.status_code != 200:
            msg = req_obj["Message"]
            raise Exception(f"{req.status_code}. Issue retrieving completed activities: {msg}")

        if not req_obj:
            raise Exception("Completed activies is empty")

        return req_obj

    def get_completed_activity_status(self, model_name, activity_id):
        """
        Gets the status of a completed activity by its id
        :param model_name:
        :param activity_id (integer):
        :return:
        """
        activity_list = self.get_all_completed_activities(model_name)
        res = {}
        for dic in activity_list:
            if dic["progressId"] == int(activity_id):
                res["message"] = dic["message"]
                res["value"] = dic["status"]
                break

        if not res:
            raise Exception("Invalid activity id specified or activity id is not complete")
        return res

    def monitor_activity(self, model_name, activity_id, interval_mins=0.1):
        """
        Monitors an activity untill its status <> "Running"
        :param model_name:
        :param activity_id:
        :param interval_mins:
        :return:
        """
        status = self.get_live_activity_status(model_name, activity_id)
        run_status = status["message"]
        percentage = status["value"]
        if status["value"] != 'Completed':
            log.info("Starting polling loop")
            log.info("Current status: %s - %s", run_status, percentage)
        while run_status == "Running":
            time.sleep(60 * interval_mins)
            status = self.get_live_activity_status(model_name, activity_id)
            run_status = status["message"]
            percentage = status["value"]
            if status["value"] != 'Completed':
                log.info("Current status: %s - %s", run_status, percentage)

        status2 = self.get_completed_activity_status(model_name=model_name, activity_id=activity_id)
        final_status = status2["message"]
        log.info("Final status: %s", final_status)
        log.info("Your job is complete!!!!!")


def exec_runner(model_name, process_name, **kwargs):
    """
    light wrapper for command line execution
    :param model_name:
    :param job_name:
    :param interval (optional, minutes, default is 0.1min/6s):
    :param username (optional, use api key instead):
    :param password (optional, use api key instead):
    :param api_key (optional, use username/password instead):
    :return:
    """
    api_key = kwargs.get('api_key', None)
    username = kwargs.get('username', None)
    password = kwargs.get('password', None)
    interval_mins = kwargs.get('interval_mins', 0.1)

    job_runner = Runner(api_key)

    if not api_key or not password:
        raise Exception("API Key or Password missing")

    if not api_key:
        job_runner.get_token(username=username, password=password)
    activity_id = job_runner.run_process_by_name(model_name=model_name,
                                                 process_name=process_name)
    job_runner.monitor_activity(model_name=model_name,
                                activity_id=activity_id, interval_mins=interval_mins)


if __name__ == "__main__":
    PARSER.add_argument("-u", "--username", help="icm username")
    PARSER.add_argument("-p", "--password", help="icm username")
    PARSER.add_argument("-a", "--api_key", help="api key")
    PARSER.add_argument("-m", "--model_name", help="model name, icm environment")
    PARSER.add_argument("-j", "--job_name", help="the name of the job/process you want to run")
    ARGS = PARSER.parse_args()

    if not ARGS.api_key:
        exec_runner(username=ARGS.username, password=ARGS.password,
                    model_name=ARGS.model_name, process_name=ARGS.job_name)
    else:
        exec_runner(api_key=ARGS.api_key, model_name=ARGS.model_name,
                    process_name=ARGS.job_name)
