import logging

from flask import Blueprint, jsonify, request, render_template

from app.services.user_service import UserService

logger = logging.getLogger(__name__)


def create_app_routes(user_service: UserService):
    app_routes = Blueprint("app", __name__)

    @app_routes.route('/home', methods=['GET'])
    def home():
        return render_template('home.html')
    
    @app_routes.route('/admin-home', methods=['GET'])
    def admin_home():
        return render_template('home-admin.html')
    
    @app_routes.route('/remove-account', methods=['PUT'])
    def remove_account():
        user_query = request.form.get('q')
        user_service.remove_user_account(user_query)
        
    @app_routes.route('/user-profile-admin-view', methods=['GET'])
    def user_profile_admin_view():
        email = request.args.get('email')
        
        if email:
            email_results = user_service.get_user_by_email(email)
        else:
            # Will need to handle this properly later
            return render_template('404.html')
            
        return render_template('user-profile-page-admin-view.html', result=email_results)

    
    @app_routes.route('/user-profile', methods=['GET'])
    def user_profile():
        email = request.args.get('email')
        
        if email:
            email_results = user_service.get_user_by_email(email)
        else:
            # Will need to handle this properly later
            return render_template('404.html')
            
        return render_template('user-profile-page.html', result=email_results)


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

    @app_routes.route('/user-search-live', methods=['GET'])
    def user_search_live():
        user_query = request.args.get('q')
        
        name_results = user_service.get_user_by_name(user_query)
        if name_results:
            return jsonify(name_results)

        email_results = user_service.get_user_by_email(user_query)
        if email_results:
            return jsonify(email_results)

        slack_results = user_service.get_user_by_slack_username(user_query)
        if slack_results:
            return jsonify(slack_results)

        github_results = user_service.get_user_by_github_username(user_query)
        if github_results:
            return jsonify(github_results)

        return jsonify([])

    return app_routes
