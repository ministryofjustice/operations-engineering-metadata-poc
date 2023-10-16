from flask import Blueprint, jsonify

from app.services.user_service import UserService


def create_api_route(user_service: UserService):
    api_route = Blueprint("api", __name__)

    @api_route.route("/api/user/email/<email>", methods=["GET"])
    def get_user_by_email(email: str):
        return jsonify(user_service.get_user_by_email(email))

    @api_route.route("/api/user/slack-username/<slack_username>", methods=["GET"])
    def get_user_by_slack_username(slack_username: str):
        return jsonify(user_service.get_user_by_slack_username(slack_username))

    @api_route.route("/api/user/github-username/<github_username>", methods=["GET"])
    def get_user_by_github_username(github_username: str):
        return jsonify(user_service.get_user_by_github_username(github_username))

    return api_route
