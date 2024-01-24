from dataclasses import dataclass
from typing import Type, List

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
    name: str = db.Column(
        db.String(100), unique=False, nullable=False)
    docker: bool = db.Column(db.Boolean, nullable=False)
    pagerduty: bool = db.Column(db.Boolean, nullable=False)
    sentry: bool = db.Column(db.Boolean, nullable=False)
    pingdom: bool = db.Column(db.Boolean, nullable=False)


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
                              github_username='test_user_1_github_username',
                              name='Test Userone'))
                self.__session.add(
                    UserModel(email='test_user_2_email@digital.justice.gov.uk',
                              slack_username='test_user_2_slack_username',
                              github_username='test_user_2_github_username',
                              name='Test Usertwo'))
                self.__session.add(
                    UserModel(email='test_user_3_email@digital.justice.gov.uk',
                              slack_username='test_user_3_slack_username',
                              github_username='test_user_3_github_username',
                              name = 'Test Userthree'))
            self.__session.commit()

    def get_user_by_email(self, email: str) -> List[Type[UserModel]] | None:
        return self.__session.query(UserModel).filter(UserModel.email.ilike(f"%{email}%")).all()

    def get_user_by_slack_username(self, slack_username: str) -> List[Type[UserModel]] | None:
        return self.__session.query(UserModel).filter(UserModel.slack_username.ilike(f"%{slack_username}%")).all()

    def get_user_by_github_username(self, github_username: str) -> List[Type[UserModel]] | None:
        return self.__session.query(UserModel).filter(UserModel.github_username.ilike(f"%{github_username}%")).all()
    
    def get_user_by_name(self, name: str) -> List[Type[UserModel]] | None:
        return self.__session.query(UserModel).filter(UserModel.name.ilike(f"%{name}%")).all()

    def add_users(self, users: list[dict], allowed_users: list[str]):
        for user in users:
            if user['github_username'] in allowed_users:
                self.__add_user(
                    user['email'], 
                    user['slack_username'], 
                    user['github_username'], 
                    user['name'],
                    user['docker'],
                    user['pagerduty'],
                    user['sentry'],
                    user['pingdom'])
            else:
                self.app.logger.warning(
                    f'skipping user [{user["github_username"]}] - not in allowed list')
        self.__session.commit()

    def __add_user(self, email: str, slack_username: str, github_username: str, name: str, 
                   docker: bool, pagerduty: bool, sentry: bool, pingdom: bool) -> None:
        self.__session.add(UserModel(email=email,
                                     slack_username=slack_username,
                                     github_username=github_username,
                                     name=name,
                                     docker=docker,
                                     pagerduty=pagerduty,
                                     sentry=sentry,
                                     pingdom=pingdom))

    def delete_all_users(self) -> int:
        rows_deleted = self.__session.query(UserModel).delete()
        self.__session.commit()
        return rows_deleted
