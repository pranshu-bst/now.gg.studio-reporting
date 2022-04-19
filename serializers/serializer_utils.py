from datetime import datetime


def serialize_before_save(obj):
    if not obj.get("modified_at"):
        obj['modified_at'] = datetime.utcnow()
    return obj


def serialize_json_object(json_object):
    json_object['id'] = json_object['_id']['$oid']
    json_object.pop('_id')
    json_object['created_at'] = json_object['created_at']['$date'] if json_object.get('created_at') else None
    json_object['modified_at'] = json_object['modified_at']['$date'] if json_object.get('modified_at') else\
        json_object['created_at']
    return json_object
