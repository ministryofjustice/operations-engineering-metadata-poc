import unittest
from unittest.mock import MagicMock

from app import DBClient
from app.services.user_service import UserService
from app.tests.test_data import user_1, user_2, user_3, users_post_data


class TestGetUserByEmail(unittest.TestCase):

    def test_returns_user_if_present(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_email.return_value = user_3
        found_user = UserService(
            mock_db_client).get_user_by_email(user_3.email)
        self.assertEqual(user_3, found_user)

    def test_returns_nothing_if_not_found(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_email.return_value = None
        found_user = UserService(
            mock_db_client).get_user_by_email("unknown_email")
        self.assertIsNone(found_user)

    def test_returns_all_matching_users(self):
        search_query = "email"
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_email.return_value = [
            user_1, user_2, user_3]
        found_users = UserService(
            mock_db_client).get_user_by_email(search_query)

        expected_users = [user_1, user_2, user_3]
        self.assertListEqual(expected_users, found_users)


class TestGetUserBySlackUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_slack_username.return_value = user_1
        found_user = UserService(mock_db_client).get_user_by_slack_username(
            user_1.slack_username)
        self.assertEqual(user_1, found_user)

    def test_returns_nothing_if_not_found(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_slack_username.return_value = None
        found_user = UserService(mock_db_client).get_user_by_slack_username(
            "unknown_slack_username")
        self.assertIsNone(found_user)

    def test_returns_all_matching_users(self):
        search_query = "slack"
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_slack_username.return_value = [
            user_1, user_2, user_3]
        found_users = UserService(
            mock_db_client).get_user_by_slack_username(search_query)

        expected_users = [user_1, user_2, user_3]
        self.assertListEqual(expected_users, found_users)


class TestGetUserByGithubUsername(unittest.TestCase):

    def test_returns_user_if_present(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_github_username.return_value = user_2
        found_user = UserService(mock_db_client).get_user_by_github_username(
            user_2.github_username)
        self.assertEqual(user_2, found_user)

    def test_returns_nothing_if_not_found(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_github_username.return_value = None
        found_user = UserService(mock_db_client).get_user_by_github_username(
            "unknown_github_username")
        self.assertIsNone(found_user)

    def test_returns_all_matching_users(self):
        search_query = "github"
        mock_db_client = MagicMock(DBClient)
        mock_db_client.get_user_by_github_username.return_value = [
            user_1, user_2, user_3]
        found_users = UserService(
            mock_db_client).get_user_by_github_username(search_query)

        expected_users = [user_1, user_2, user_3]
        self.assertListEqual(expected_users, found_users)


class TestAddUsers(unittest.TestCase):

    def test_calls_downstream_services(self):
        mock_db_client = MagicMock(DBClient)
        UserService(mock_db_client).add_users(
            users_post_data)
        mock_db_client.add_users.assert_called_once_with(
            users_post_data, [
                'connormaglynn',
                'PepperMoJ',
                'githubgary',
                'githubgeorge',
                'KeithTheCoder',
                'DaveTheCoder',
                'sarahsaurus',
                'PaulRudd',
                'PaulRudd2',
                'jasonBirchall'
            ])


class TestDeleteAllUsers(unittest.TestCase):

    def test_returns_number_of_rows_deleted_as_string(self):
        mock_db_client = MagicMock(DBClient)
        mock_db_client.delete_all_users.return_value = 3
        response = UserService(mock_db_client).delete_all_users()
        self.assertEqual("3", response)

    def test_calls_downstream_services(self):
        mock_db_client = MagicMock(DBClient)
        UserService(mock_db_client).delete_all_users()
        mock_db_client.delete_all_users.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
