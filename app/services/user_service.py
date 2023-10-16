from app.clients.db_client import DBClient


class UserService:
    def __init__(self, db_client: DBClient):
        self.__db_client = db_client

    def get_user_by_email(self, email: str):
        return self.__db_client.get_user_by_email(email)

    def get_user_by_slack_username(self, slack_username: str):
        return self.__db_client.get_user_by_slack_username(slack_username)

    def get_user_by_github_username(self, github_username: str):
        return self.__db_client.get_user_by_github_username(github_username)
