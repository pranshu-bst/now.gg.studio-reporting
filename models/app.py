from datetime import datetime
import os
from mongoengine import *
import constants

MONGO_URI = os.environ.get('MONGO_URI')
connect(host=MONGO_URI)
AppStatus = (constants.AppStatus.DISABLED, constants.AppStatus.ACTIVE)


class OauthKeys(EmbeddedDocument):
    env_type = StringField(required=True)
    client_id = StringField(required=True)
    client_secret = StringField(required=True)


class NftKeys(EmbeddedDocument):
    env_type = StringField(required=True)
    token = StringField(required=True)


class App(Document):
    app_id = StringField(required=True)
    app_title = DictField(required=True)
    app_pkg_name = StringField(required=True, unique=True, max_length=100)
    company_id = StringField(required=True)
    oauth_keys = EmbeddedDocumentListField(OauthKeys, default=[])
    nft_keys = EmbeddedDocumentListField(NftKeys, default=[])
    tier = StringField(choices=constants.ModelChoices.APP_TIERS, default=constants.AppTiers.ECONOMY)
    created_at = DateTimeField(default=datetime.utcnow)
    iap_integration = BooleanField(default=False)
    login_integration = BooleanField(default=False)
    nft_integration = BooleanField(default=False)
    tags = ListField(default=[])
    status = StringField(choices=AppStatus, default=constants.AppStatus.ACTIVE)
    modified_at = DateTimeField()
    meta = {'collection': 'App'}
