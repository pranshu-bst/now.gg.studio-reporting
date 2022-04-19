from datetime import datetime

from mongoengine import *
import constants
import constants

MONGO_URI = constants.MONGO_URI
connect(host=MONGO_URI)

SubmissionType = (constants.SubmissionType.FULL, constants.SubmissionType.METADATA_CHANGE)

SubmissionStates = (constants.SubmissionStates.DRAFT, constants.SubmissionStates.SUBMITTED,
                    constants.SubmissionStates.UNDER_TESTING, constants.SubmissionStates.READY_FOR_PUBLISHING,
                    constants.SubmissionStates.PUBLISHED, constants.SubmissionStates.UNPUBLISHED,
                    constants.SubmissionStates.ARCHIVED)

AppAssetsSource = (constants.AppAssetsSource.MANUAL, constants.AppAssetsSource.GOOGLE_PLAY_STORE)

APKSource = (constants.APKSource.LINK, constants.APKSource.GOOGLE_PLAY_LINK, constants.APKSource.UPLOAD_FILE)


class AppAssetsMetadata(EmbeddedDocument):
    asset_category = StringField(default='')
    asset_type = StringField(default='')
    asset_url = StringField(default='')


class AppAssetsMapping(EmbeddedDocument):
    lang = StringField(default='')
    data = EmbeddedDocumentListField(AppAssetsMetadata)


class AppDeveloperInfo(EmbeddedDocument):
    official_email_id = StringField(default='')
    official_website = StringField(default='')
    developer_name = StringField(default='')
    terms_of_services = StringField(default='')
    privacy_policy = StringField(default='')


class Comment(EmbeddedDocument):
    comment_text = StringField(required=True)
    commented_by = StringField(required=True)
    from_state = StringField(required=True)
    to_state = StringField(required=True)
    commented_at = DateTimeField(required=True)


class SslMapping(EmbeddedDocument):
    name = StringField(required=True)
    ssl_type = StringField(required=True)
    value = StringField(required=True)


class DomainMapping(EmbeddedDocument):
    name = StringField(required=True)
    domain_type = StringField(required=True)
    value = StringField(required=True)


class SslKey(EmbeddedDocument):
    ssl_mapping = EmbeddedDocumentField(SslMapping, required=True, default={})
    domain_mapping = EmbeddedDocumentField(DomainMapping, required=True, default={})


class AppSubmission(Document):
    app_id = StringField(required=True)
    submission_type = StringField(choices=SubmissionType, default=constants.SubmissionType.FULL)
    submission_state = StringField(choices=SubmissionStates, required=True)
    app_version = StringField(default='')
    app_version_code = IntField(null=True)
    app_title = DictField(default={})
    app_pkg_name = StringField(default='')
    app_description = DictField(default={})
    app_assets = EmbeddedDocumentListField(AppAssetsMapping)
    app_assets_source = StringField(choices=AppAssetsSource, default='')
    app_playstore_url = StringField(default='')
    app_playstore_apk_url = StringField(default='')
    app_published_regions = DictField(default={})
    app_category = DictField(default={})
    app_sub_category = DictField(default={})
    app_developer_info = EmbeddedDocumentField(AppDeveloperInfo, default={})
    apk_source = StringField(choices=APKSource, default='')
    uploaded_apk_url = StringField(default='')
    dev_apk_link = StringField(default='')
    live_apk_url = StringField(default='')
    app_testing_url = StringField(default='')
    app_prod_url = StringField(default='')
    custom_domain_url = StringField(default='')
    comments = EmbeddedDocumentListField(Comment, default=[])
    ssl_keys = EmbeddedDocumentField(SslKey, default={})
    created_by = StringField(default='')
    last_updated_by = StringField(default='')
    iap_integration = BooleanField(default=False)
    login_integration = BooleanField(default=False)
    nft_integration = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    modified_at = DateTimeField()
    meta = {'collection': 'AppSubmission'}
