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
        pass

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
        pass

    def test_get_all_completed_activities(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_get_completed_activity_status(self, mock_req):
        """

        :param mock_post:
        :return:
        """
        pass


if __name__ == '__main__':
    import unittest as ut
    ut.main()

