from unittest import TestCase
from unittest.mock import patch
from icm_runner import Runner


@patch('icm_runner.requests')
class TestRunner(TestCase):
    """

    """

    def test_get_token(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        mock_req.post.return_value.json.return_value = {'token': 'blah'}
        mock_req.post.return_value.status_code = 200
        Runner().get_token('', '')

    def test_build_header(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        fixture_header = {'authorization': 'bearer ', 'model': 'fake_model', 'content-type': 'application/json'}
        header = Runner().build_header('fake_model')
        self.assertEqual(fixture_header, header)

    def test_get_process_id(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        mock_req.get.return_value.json.return_value = \
            [{'activation': 'Enabled',
              'childScheduleItems': [],
              'id': 1,
              'lastRun': '2019-02-01T12:10:33.757Z',
              'lastRunStatus': 'Success',
              'name': 'test1',
              'nextRun': '0001-01-01T00:00:00',
              'order': 1,
              'scheduleItemType': 'Folder',
              'settings': {'emailOnFailure': True,
                           'emailOnSuccess': True,
                           'enableRetries': False,
                           'externalToolTimeout': 0,
                           'failEmails': ['test@test.com'],
                           'isGlobal': False,
                           'overrideChildSettings': False,
                           'scheduleItemId': 1,
                           'schedulerSettingsId': 7,
                           'stopOnFailure': True,
                           'stopToolOnTimeout': False,
                           'successEmails': ['test@test.com'],
                           'version': {'rowVersion': 1}},
              'version': {'rowVersion': 1}}, ]
        mock_req.get.return_value.status_code = 200
        activity_id = Runner().get_process_id('test', 'test1')
        self.assertEqual(int(activity_id), 1)


    def test_run_process_by_id(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        mock_req.post.return_value.json.return_value = \
            {'completedactivities': 'api/v1/completedactivities/1',
              'liveactivities': 'api/v1/liveactivities/1'}
        mock_req.post.return_value.status_code = 200
        activity_id = Runner().run_process_by_id('test', '1')
        self.assertEqual(int(activity_id), 1)

    def test_run_process_by_name(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_get_live_activity_status(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        mock_req.get.return_value.json.return_value = \
            [{'progressId': 1,
              'userId': 'test',
              'type': 'Calculation',
              'status': 'Running',
              'time': '2019-10-08T19:54:23.76Z',
              'percent': 99,
              'description': 'TEST 007 Get Record Counts Sorted by Date Desc',
              'hasDescription': True,
              'expiresAt': '2019-10-08T20:04:57.123Z',
              'isCancellable': True,
              'isInitialization': False,
              'computationId': 1},
             {'progressId': 1,
              'userId': 'test',
              'type': 'Scheduler',
              'status': 'Running',
              'time': '2019-10-08T19:54:23.51Z',
              'percent': 0,
              'description': 'Executing scheduler item...',
              'hasDescription': True,
              'expiresAt': '2019-10-08T20:04:56.95Z',
              'isCancellable': True,
              'isInitialization': False,
              'computationId': -1}, ]
        mock_req.get.return_value.status_code = 200
        mock_res = {'message': 'Running', 'value': 99}
        res = Runner().get_live_activity_status('test', '1')
        self.assertEqual(mock_res, res)

    def test_get_all_completed_activities(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        mock_req.get.return_value.json.return_value = \
            [{'progressId': 1,
              'userId': 'test@test.com',
              'type': 'Calculation',
              'status': 'Completed',
              'message': 'TEST 103 Get Sessions with Missing Rates calculated successfully.',
              'time': '2019-09-27T16:44:51.573Z',
              'messageDetails': ''}, ]
        mock_req.get.return_value.status_code = 200
        mock_res = \
            [{'progressId': 1,
              'userId': 'test@test.com',
              'type': 'Calculation',
              'status': 'Completed',
              'message': 'TEST 103 Get Sessions with Missing Rates calculated successfully.',
              'time': '2019-09-27T16:44:51.573Z',
              'messageDetails': ''}, ]
        res = Runner().get_all_completed_activities('test')
        self.assertEqual(mock_res, res)

    def test_get_completed_activity_status(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_monitor_activity(self, mock_req):
        """"

        :param mock_post:
        :return:
        """
        pass

if __name__ == '__main__':
    import unittest as ut
    ut.main()

