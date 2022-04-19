import json
from queries.company import CompanyQueries
from queries.user_account import UserAccountQueries
from queries.app import AppQueries
from queries.app_submission import AppSubmissionQueries

user_tnc_accepted_rawfile = "user_tnc_accepted_rawfile.json"

def get_user_tnc_time_map():
    file = open(user_tnc_accepted_rawfile)
    sheet_as_json = json.load(file)
    file.close()
    user_tnc_time_map = dict()
    for item in sheet_as_json:
        user_tnc_time_map[item["email"]] = {
            "tnc_accepted_via":item["action_user_type"],
            "tnc_accepted_time":item["accepted_at"],
        }
    return user_tnc_time_map

def get_users_map():
    user_account_collection = UserAccountQueries()
    users, users_count = user_account_collection.get_paginated_user_list(sort_order=["-modified_at"])
    return users

result = get_users_map()
print(result)