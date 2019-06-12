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

class Runner:
    """
    The main class that contains the required ICM API Call
    Functions to manage running the Scheduler
    """
    def __init__(self):
        """
        Intializes a class
        """
        self.login_url = f"{SPM_URL}/services/login"
        self.token = ""

    def get_token(self, username, password):
        """
        Gets the token needed for making api calls
        :param username:
        :param password:
        :return:
        """
        log.info('getting token for %s', username)
        call_data = {
            "email": username,
            "password": password,
            "content-type": "application/json"
        }
        req = requests.post(url=self.login_url, data=call_data)
        req_obj = req.json()
        if "token" in req_obj.keys():
            log.info("token obtained successfuly.")
            self.token = req_obj["token"]
        else:
            raise Exception(f'issue getting token: {req_obj}')

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
        if req.text == "" or req.status_code == 401:
            raise Exception("Model name does not exist.")

        for i in req.json():
            if i['name'] == process_name:
                process_id = str(i['id'])
                log.info('process id = %s', process_id)
                break
        if process_id == -1:
            raise Exception("Process name does not exist.")
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
        if "liveactivities" in req_obj.keys():
            log.info("Process run scheduled (immediate) successfully.")
            activity = req_obj["liveactivities"]
            pos = len(activity) - activity.rfind("/", 1, 9999) - 1
            activity_id = activity[-pos:]
        elif "Message" in req_obj.keys():
            raise Exception('Issue scheduling process: {}'.format(req_obj["Message"]))
        else:
            raise Exception("Something is not right."
                            "Check the json object in the returned results 'request' key value.")
        log.info('activity id = %s', activity_id)

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
        if req.text == "" or req.status_code == 401:
            raise Exception("Model name does not exist.")
        if not req_obj:
            res["message"] = "Activity ID does not exist or is no longer active."
            res["value"] = 100
        else:
            for dic in req_obj:
                if "type" in dic.keys():
                    res["message"] = dic["status"]
                    res["value"] = dic["percent"]
                    break
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
        if req.text == "" or req.status_code == 401:
            raise Exception("Model name does not exist.")
        res = req.json()
        return res

    def get_completed_activity_status(self, model_name, activity_id):
        """
        Gets the status of a completed activity by its id
        :param model_name:
        :param activity_id:
        :return:
        """
        activity_list = self.get_all_completed_activities(model_name)
        res = {}
        for dic in activity_list:
            if dic["progressId"] == int(activity_id):
                if "errors" in dic["message"]:
                    res["message"] = dic['message']
                    res["value"] = dic["status"]
                else:
                    res["message"] = dic["message"]
                    res["value"] = dic["status"]
                break
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
        run_status = status['message']
        percentage = status['value']
        log.info('starting polling loop')
        log.info("current status: %s - %s ", run_status, percentage)
        while run_status == "Running":
            time.sleep(60 * interval_mins)
            status = self.get_live_activity_status(model_name, activity_id)
            run_status = status['message']
            percentage = status['value']
            log.info("current status: %s - %s ", run_status, percentage)

        status2 = self.get_completed_activity_status(model_name=model_name, activity_id=activity_id)
        final_status = status2['message']
        log.info('final status: %s', final_status)
        log.info('your job is complete!!!!!')


def exec_runner():
    """
    light wrapper for command line execution
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="icm username")
    parser.add_argument("-p", "--password", help="icm username")
    parser.add_argument("-m", "--model_name", help="model name, icm environment")
    parser.add_argument("-j", "--job_name", help="the name of the job/process you want to run")
    args = parser.parse_args()

    job_runner = Runner()

    job_runner.get_token(username=args.username, password=args.password)
    activity_id = job_runner.run_process_by_name(model_name=args.model_name,
                                          process_name=args.job_name)
    job_runner.monitor_activity(model_name=args.model_name,
                                activity_id=activity_id, interval_mins=0.1)


if __name__ == "__main__":
    exec_runner()
