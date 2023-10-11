from dataclasses import dataclass


@dataclass
class User:
    email: str
    slack_username: str
    github_username: str


class UserService:
    def __init__(self, stubbed_users=None):
        if stubbed_users is None:
            stubbed_users = []
        self.__stubbed_users = stubbed_users or [
            User(slack_username="test_user_1_slack", github_username="test_user_1_github",
                 email="test_user_1_email@digital.justice.gov.uk"),
            User(slack_username="test_user_2_slack", github_username="test_user_2_github",
                 email="test_user_2_email@digital.justice.gov.uk"),
            User(slack_username="test_user_3_slack", github_username="test_user_3_github",
                 email="test_user_3_email@digital.justice.gov.uk"),
        ]

    def get_user_by_email(self, email: str):
        for user in self.__stubbed_users:
            if user.email == email:
                return user

    def get_user_by_slack_username(self, slack_username: str):
        for user in self.__stubbed_users:
            if user.slack_username == slack_username:
                return user

    def get_user_by_github_username(self, github_username: str):
        for user in self.__stubbed_users:
            if user.github_username == github_username:
                return user
