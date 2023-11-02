import logging

from flask import Blueprint, request, render_template

from app.services.user_service import UserService

logger = logging.getLogger(__name__)


def create_app_routes(user_service: UserService):
    app_routes = Blueprint("app", __name__)

    @app_routes.route('/home', methods=['GET'])
    def home():
        return render_template('home.html')

    @app_routes.route('/user-search', methods=['POST'])
    def user_search():
        user_query = request.form.get('q')

        email_results = user_service.get_user_by_email(user_query)

        if email_results:
            return render_template('search-results.html', results=email_results, user_query=user_query)

        slack_results = user_service.get_user_by_slack_username(user_query)

        if slack_results:
            return render_template('search-results.html', results=slack_results, user_query=user_query)

        github_results = user_service.get_user_by_github_username(user_query)

        if github_results:
            return render_template('search-results.html', results=github_results, user_query=user_query)

        return render_template('search-results.html', results=None, user_query=user_query)

    return app_routes
