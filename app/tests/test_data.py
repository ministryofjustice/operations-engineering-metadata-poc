from app.clients.db_client import UserModel

user_1 = UserModel(slack_username="test_user_1_slack", github_username="test_user_1_github",
                   email="test_user_1_email@digital.justice.gov.uk")
user_2 = UserModel(slack_username="test_user_2_slack", github_username="test_user_2_github",
                   email="test_user_2_email@digital.justice.gov.uk")
user_3 = UserModel(slack_username="test_user_3_slack", github_username="test_user_3_github",
                   email="test_user_3_email@digital.justice.gov.uk")

stubbed_users = [user_1, user_2, user_3]
