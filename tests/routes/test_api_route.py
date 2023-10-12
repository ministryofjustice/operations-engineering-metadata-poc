import json
import unittest

import app
from app.services.user_service import User
from tests.test_data import user_1, user_2, user_3


class TestGetUserByEmail(unittest.TestCase):

    def test_returns_user_if_present(self):
        response = json.loads(app.create_app().test_client().get(
            f'/api/user/email/{user_1.email}').data)
        self.assertEqual(user_1, User(**response))


class TestGetUserBySlackUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        response = json.loads(app.create_app().test_client().get(
            f'/api/user/slack-username/{user_2.slack_username}').data)
        self.assertEqual(user_2, User(**response))


class TestGetUserByGithubUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        response = json.loads(app.create_app().test_client().get(
            f'/api/user/github-username/{user_3.github_username}').data)
        self.assertEqual(user_3, User(**response))


if __name__ == "__main__":
    unittest.main()
