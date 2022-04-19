import json

from serializers.serializer_utils import serialize_json_object


def _serialize_app_json_object(app_json_object):
    app_json_object['iap_integration'] = app_json_object['iap_integration'] if app_json_object.get(
        'iap_integration') else False
    app_json_object['login_integration'] = app_json_object['login_integration'] if app_json_object.get(
        'login_integration') else False
    app_json_object['nft_integration'] = app_json_object['nft_integration'] if app_json_object.get(
        'nft_integration') else False
    app_json_object['status'] = app_json_object['status'] if app_json_object.get(
        'status') else True
    app_json_object['tags'] = app_json_object['tags'] if app_json_object.get(
        'tags') else []
    return app_json_object


def serialize_app(obj):
    if not obj:
        return None

    json_object = json.loads(obj.to_json())
    if isinstance(json_object, list):
        return [_serialize_app_json_object(serialize_json_object(json_obj)) for json_obj in json_object]
    else:
        return _serialize_app_json_object(serialize_json_object(json_object))
