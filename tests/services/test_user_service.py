import unittest

from app.services.user_service import UserService
from tests.test_data import stubbed_users, user_1, user_2, user_3


class TestGetUserByEmail(unittest.TestCase):

    def test_returns_user_if_present(self):
        found_user = UserService(stubbed_users).get_user_by_email(user_3.email)
        self.assertEqual(user_3, found_user)

    def test_returns_nothing_if_not_found(self):
        found_user = UserService(
            stubbed_users).get_user_by_email("unknown_email")
        self.assertIsNone(found_user)


class TestGetUserBySlackUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        found_user = UserService(stubbed_users).get_user_by_slack_username(
            user_1.slack_username)
        self.assertEqual(user_1, found_user)

    def test_returns_nothing_if_not_found(self):
        found_user = UserService(stubbed_users).get_user_by_slack_username(
            "unknown_slack_username")
        self.assertIsNone(found_user)


class TestGetUserByGithubUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        found_user = UserService(stubbed_users).get_user_by_github_username(
            user_2.github_username)
        self.assertEqual(user_2, found_user)

    def test_returns_nothing_if_not_found(self):
        found_user = UserService(stubbed_users).get_user_by_slack_username(
            "unknown_github_username")
        self.assertIsNone(found_user)


if __name__ == "__main__":
    unittest.main()
