from app.clients.db_client import DBClient


class UserService:
    def __init__(self, db_client: DBClient, allowed_users=None):
        self.__db_client = db_client
        # TODO: Temporary security measure, just to ensure the database doesn't get spammed. We should migrate to a proper authentication flow
        if allowed_users is None:
            allowed_users = [
                'connormaglynn',
                'PepperMoJ',
                'githubgary',
                'githubgeorge',
                'KeithTheCoder',
                'DaveTheCoder',
                'sarahsaurus',
                'PaulRudd',
                'PaulRudd2'
            ]
        self.__allowed_users = allowed_users

    def get_user_by_email(self, email: str):
        return self.__db_client.get_user_by_email(email)

    def get_user_by_slack_username(self, slack_username: str):
        return self.__db_client.get_user_by_slack_username(slack_username)

    def get_user_by_github_username(self, github_username: str):
        return self.__db_client.get_user_by_github_username(github_username)

    def add_users(self, users: list[dict]):
        self.__db_client.add_users(users, self.__allowed_users)

    def delete_all_users(self) -> str:
        return str(self.__db_client.delete_all_users())
