import json

import constants
from serializers.serializer_utils import serialize_json_object


def _serialize_app_submission_json_object(app_submission):
    app_submission['ssl_keys'] = app_submission['ssl_keys'] if app_submission.get(
        'ssl_keys') else {}
    app_submission['iap_integration'] = app_submission['iap_integration']\
        if app_submission.get('iap_integration') else False
    app_submission['login_integration'] = app_submission['login_integration']\
        if app_submission.get('login_integration') else False
    app_submission['nft_integration'] = app_submission['nft_integration']\
        if app_submission.get('nft_integration') else False

    app_submission['apk_source'] = app_submission['apk_source']\
        if app_submission.get('apk_source') else ""
    if app_submission['apk_source'] == constants.APKSource.GOOGLE_PLAY_LINK:
        app_submission['apk_source'] = "google_play_link"

    if not app_submission.get('app_playstore_apk_url'):
        if app_submission['apk_source'] == "google_play_link":
            app_submission['app_playstore_apk_url'] = app_submission['app_playstore_url']
        else:
            app_submission['app_playstore_apk_url'] = ""

    return app_submission


def serialize_app_submission(obj):
    if not obj:
        return None

    json_object = json.loads(obj.to_json())
    if isinstance(json_object, list):
        return [_serialize_app_submission_json_object(serialize_json_object(json_obj)) for json_obj in json_object]
    else:
        return _serialize_app_submission_json_object(
            serialize_json_object(json_object))
