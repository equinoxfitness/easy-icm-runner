"""
IBM ICM API Calls Classes
Complete list: https://developer.ibm.com/api/view/id-689:title-Incentive_Compensation_Management
"""

import json
import time
import requests
import logging as log


log.basicConfig(format='%(asctime)s - %(message)s', level=log.INFO)


class Runner:
    """
    The main class that contains the required ICM API Call
    Functions to manage running the Scheduler
    """
    def __init__(self):
        """
        Intializes a class
        """
        name = "easy-icm-runner" #for packaging
        self.login_url = "https://spm.ibmcloud.com/services/login"
        self.token = ""

    def get_token(self, username, password):
        """
        Gets the token needed for making api calls
        """
        log.info(f'getting token for {username}')
        call_data = {
            "email": username,
            "password": password,
            "content-type": "application/json"
        }
        res = {}
        req = requests.post(url=self.login_url, data=call_data)
        if "token" in req.json().keys():
            res["status"] = 1
            res["message"] = "Token obtained successfuly."
            res["value"] = req.json()["token"]
            res["request"] = req.json()
            self.token = req.json()["token"]
        elif "code" in req.json().keys():
            res["status"] = 0
            res["message"] = req.json()["message"]
            res["value"] = "0"
            res["request"] = req.json()
        else:
            res["status"] = 0
            res["message"] = "Something is not right. "+ \
                "Check the json object in the returned results 'request' key value."
            res["value"] = "0"
            res["request"] = req.json()
        log.info(res)
        return res

    def get_process_id(self, model_name, process_name):
        """
        Gets the top level processe id using a given process name
        """

        url = "https://spm.ibmcloud.com/api/v1/scheduleitem"
        pid = -1
        headers = {
            "authorization": "bearer "+self.token,
            "model": model_name,
            "content-type": "application/json"
        }
        res = {}
        req = requests.get(url=url, headers=headers)
        if req.text == "" or req.status_code == 401:
            res["status"] = 0
            res["message"] = "Model name does not exist."
            res["value"] = "0"
            res["request"] = json.dumps({"status":"no valid json object was returned"})
        else:
            for i in req.json():
                if i["name"] == process_name:
                    pid = i["id"]
                    log.info(f'process id = {pid}')
                    break
            if pid == -1:
                res["status"] = 0
                res["message"] = "Process name does not exist."
                res["value"] = str(pid)
                res["request"] = req.json()
            else:
                res["status"] = 1
                res["message"] = "Process ID obtained successfuly."
                res["value"] = str(pid)
                res["request"] = req.json()
        log.info(res)
        return res

    def run_process_by_name(self, model_name, process_name, follow=False):
        """
        Runs a top level process by its name
        """
        res = self.get_process_id(model_name, process_name)
        if res['status'] == 1:
            url = "https://spm.ibmcloud.com/api/v1/rpc/scheduleitem/"+res['value']+"/run"
            headers = {
                "authorization": "bearer "+self.token,
                "model": model_name,
                "content-type": "application/json"
            }
            res = {}
            req = requests.post(url=url, headers=headers)
            if "liveactivities" in req.json().keys():
                res["status"] = 1
                res["message"] = "Process run scheduled (immediate) successfully."
                activity = req.json()["liveactivities"]
                pos = len(activity)-activity.rfind("/", 1, 9999)-1
                res["value"] = activity[-pos:]
                res["request"] = req.json()
            elif "Message" in req.json().keys():
                res["status"] = 0
                res["message"] = req.json()["Message"]
                res["value"] = "0"
                res["request"] = req.json()
            else:
                res["status"] = 0
                res["message"] = "Something is not right. "+ \
                    "Check the json object in the returned results 'request' key value."
                res["value"] = "0"
                res["request"] = req.json()
        log.info(res)

        if follow:
            self.monitor_activity(model_name=model_name,activity_id=res['value'])

        return res

    def run_process_by_id(self, model_name, process_id, follow=False):
        """
        Runs a process by its id
        """
        url = "https://spm.ibmcloud.com/api/v1/rpc/scheduleitem/"+str(process_id)+"/run"
        headers = {
            "authorization": "bearer "+self.token,
            "model": model_name,
            "content-type": "application/json"
        }
        res = {}
        req = requests.post(url=url, headers=headers)
        if "liveactivities" in req.json().keys():
            res["status"] = 1
            res["message"] = "Process run scheduled (immediate) successfully."
            activity = req.json()["liveactivities"]
            pos = len(activity)-activity.rfind("/", 1, 9999)-1
            res["value"] = activity[-pos:]
            res["request"] = req.json()
        elif "Message" in req.json().keys():
            res["status"] = 0
            res["message"] = req.json()["Message"]
            res["value"] = "0"
            res["request"] = req.json()
        else:
            res["status"] = 0
            res["message"] = "Something is not right. "+ \
                "Check the json object in the returned results 'request' key value."
            res["value"] = "0"
            res["request"] = req.json()
        log.info(res)

        if follow:
            self.monitor_activity(model_name=model_name, activity_id=res['value'])

        return res

    def get_live_activity_status(self, model_name, activity_id):
        """
        Gets the status of a live activity by its id
        """
        url = "https://spm.ibmcloud.com/api/v1/liveactivities?liveActivityDTO="+activity_id
        headers = {
            "authorization": "bearer "+self.token,
            "model": model_name,
            "content-type": "application/json"
        }
        res = {}
        res["status"] = 0
        res["message"] = "Something is not right. "+ \
                "Check the json object in the returned results 'request' key value."
        res["value"] = "0"
        res["request"] = json.dumps({"status":"no valid json object was returned"})
        req = requests.get(url=url, headers=headers)
        if req.text == "" or req.status_code == 401:
            res["status"] = 0
            res["message"] = "Model name does not exist."
            res["value"] = "0"
            res["request"] = json.dumps({"status":"no valid json object was returned"})
        elif req.text == "[]":
            res["status"] = 0
            res["message"] = "Activity ID does not exist or is no longer active."
            res["value"] = "0"
            res["request"] = json.dumps({"status":"activity id does not exist or is no "+ \
                "longer active"})
        else:
            for dic in req.json():
                if "type" in dic.keys():
                    res["status"] = 1
                    res["message"] = dic["status"]
                    res["value"] = dic["percent"]
                    res["request"] = req.json()
                    break
        return res

    def get_all_completed_activities(self, model_name):
        """
        Gets a list of all teh completed activities
        """
        url = "https://spm.ibmcloud.com/api/v1/completedactivities"
        headers = {
            "authorization": "bearer "+self.token,
            "model": model_name,
            "content-type": "application/json"
        }
        res = {}
        res["status"] = 0
        res["message"] = "Something is not right. "+ \
                "Check the json object in the returned results 'request' key value."
        res["value"] = "0"
        res["request"] = json.dumps({"status":"no valid json object was returned"})
        req = requests.get(url=url, headers=headers)
        if req.text == "" or req.status_code == 401:
            res["status"] = 0
            res["message"] = "Model name does not exist."
            res["value"] = "0"
            res["request"] = json.dumps({"status":"no valid json object was returned"})
        else:
            res["status"] = 1
            res["message"] = "Successfully obtained a list of all completed activities."
            res["value"] = "1"
            res["request"] = req.json()
        log.info(res)
        return res

    def get_activity_status(self, model_name, activity_id):
        """
        Gets the status of a completed activity by its id
        """
        res = self.get_all_completed_activities(model_name)
        if res["status"] != 0:
            for dic in res["request"]:
                if dic["progressId"] == int(activity_id):
                    if "errors" in dic["message"]:
                        res["status"] = 0
                    else:
                        res["status"] = 1
                    res["message"] = dic["message"]
                    res["value"] = dic["status"]
                    res["request"] = dic
                    break
        log.info(res)
        return res

    def monitor_activity(self, model_name, activity_id, interval_mins=0.5):
        """
        Monitors an activity untill its status <> "Running"
        """
        res = {}
        res["status"] = 0
        res["message"] = "Something is not right. "+ \
                "Check the json object in the returned results 'request' key value."
        res["value"] = "0"
        res["request"] = json.dumps({"status":"no valid json object was returned"})
        status = self.get_live_activity_status(model_name, activity_id)
        run_status = status['message']
        log.info('starting polling loop')
        log.info(f'current status: {run_status}')
        while run_status == "Running":
            time.sleep(60*interval_mins)
            status = self.get_live_activity_status(model_name, activity_id)
            run_status = status['message']
            log.info(f'current status: {run_status}')

        status2 = self.get_activity_status(model_name, activity_id)
        run_status = status['message']
        log.info(f'final status: {run_status}')
        log.info(status2)
        return status2
