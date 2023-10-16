from dataclasses import dataclass
from typing import Type

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session

from app.config import config

db = SQLAlchemy()


@dataclass
class UserModel(db.Model):
    __tablename__ = 'users'
    email: str = db.Column(db.String(80), primary_key=True,
                           unique=True, nullable=False)
    slack_username: str = db.Column(
        db.String(100), unique=True, nullable=False)
    github_username: str = db.Column(
        db.String(100), unique=True, nullable=False)


class DBClient:
    def __init__(self, app: Flask, session: Session = db.session):
        self.app = app
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config.database.user}:{config.database.password}@{config.database.endpoint}/{config.database.name}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(self.app)
        self.__session = session

        # TODO: Delete this 🔥 these are here for initially setting up the DB - we should migrate to a proper database migration tool like `alembic`.
        with self.app.app_context():
            db.create_all()
            # Check if test data already exists before trying to create it. Since all columns should be unique, recreating will fail
            if self.get_user_by_email('test_user_1_email@digital.justice.gov.uk') is None:
                self.__session.add(
                    UserModel(email='test_user_1_email@digital.justice.gov.uk',
                              slack_username='test_user_1_slack_username',
                              github_username='test_user_1_github_username'))
                self.__session.add(
                    UserModel(email='test_user_2_email@digital.justice.gov.uk',
                              slack_username='test_user_2_slack_username',
                              github_username='test_user_2_github_username'))
                self.__session.add(
                    UserModel(email='test_user_3_email@digital.justice.gov.uk',
                              slack_username='test_user_3_slack_username',
                              github_username='test_user_3_github_username'))
            self.__session.commit()

    def get_user_by_email(self, email: str) -> Type[UserModel] | None:
        return self.__session.query(UserModel).filter_by(email=email).first()

    def get_user_by_slack_username(self, slack_username: str) -> Type[UserModel] | None:
        return self.__session.query(UserModel).filter_by(slack_username=slack_username).first()

    def get_user_by_github_username(self, github_username: str) -> Type[UserModel] | None:
        return self.__session.query(UserModel).filter_by(github_username=github_username).first()

    def add_users(self, users: list[dict], allowed_users: list[str]):
        for user in users:
            if user['github_username'] in allowed_users:
                self.__add_user(
                    user['email'], user['slack_username'], user["github_username"])
            else:
                self.app.logger.warning(
                    f'skipping user [{user["github_username"]}] - not in allowed list')
        self.__session.commit()

    def __add_user(self, email: str, slack_username: str, github_username: str) -> None:
        self.__session.add(UserModel(email=email,
                                     slack_username=slack_username,
                                     github_username=github_username))
