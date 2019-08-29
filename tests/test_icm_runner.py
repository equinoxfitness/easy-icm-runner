from unittest import TestCase
from unittest.mock import patch
from icm_runner import Runner

@patch('icm_runner.requests.post')
class TestRunner(TestCase):
    """

    """

    def test_get_token(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        mock_post.return_value.json.return_value = {'token': 'blah'}
        mock_post.return_value.status_code = 200
        Runner().get_token('', '')

    def test_build_header(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        fixture_header = {'authorization': 'bearer ', 'model': 'fake_model', 'content-type': 'application/json'}
        header = Runner().build_header('fake_model')
        self.assertEqual(fixture_header, header)

    def test_get_process_id(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_run_process_by_id(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_run_process_by_name(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_get_live_activity_status(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_get_all_completed_activities(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        pass

    def test_get_completed_activity_status(self, mock_post):
        """

        :param mock_post:
        :return:
        """
        pass


if __name__ == '__main__':
    import unittest as ut
    ut.main()

