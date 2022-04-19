import json

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

print(get_user_tnc_time_map())