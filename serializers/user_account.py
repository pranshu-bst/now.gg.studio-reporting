import json
from serializers.serializer_utils import serialize_json_object


def serialize_user_account(obj):
    if not obj:
        return None

    json_object = json.loads(obj.to_json())
    if isinstance(json_object, list):
        return [serialize_json_object(json_obj) for json_obj in json_object]
    else:
        return serialize_json_object(json_object)
