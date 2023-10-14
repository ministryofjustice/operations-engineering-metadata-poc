import json
import unittest
from unittest.mock import MagicMock

import app
from app.clients.db_client import DBClient, UserModel
from app.tests.test_data import user_1, user_2, user_3


class TestGetUserByEmail(unittest.TestCase):

    def test_returns_user_if_present(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_email.return_value = user_1
        response = json.loads(app.create_app(mock_db_client).test_client().get(
            f'/api/user/email/{user_1.email}').data)
        self.assertEqual(user_1, UserModel(**response))


class TestGetUserBySlackUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_slack_username.return_value = user_2
        response = json.loads(app.create_app(mock_db_client).test_client().get(
            f'/api/user/slack-username/{user_2.slack_username}').data)
        self.assertEqual(user_2, UserModel(**response))


class TestGetUserByGithubUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_github_username.return_value = user_3
        response = json.loads(app.create_app(mock_db_client).test_client().get(
            f'/api/user/github-username/{user_3.github_username}').data)
        self.assertEqual(user_3, UserModel(**response))


if __name__ == "__main__":
    unittest.main()
