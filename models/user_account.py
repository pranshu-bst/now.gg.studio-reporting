from datetime import datetime
import os
from mongoengine import *
import constants

MONGO_URI = os.environ.get('MONGO_URI')
connect(host=MONGO_URI)
AccountType = (constants.AccountType.CUSTOMER, constants.AccountType.SALES_REP)
UserStatus = (constants.UserStatus.PENDING, constants.UserStatus.APPROVED)
UserAccountStatus = (constants.UserAccountStatus.DISABLED, constants.UserAccountStatus.ACTIVE)


class UserAccount(Document):
    company_ids = ListField(default=[])
    email = StringField(required=True, unique=True)
    account_type = StringField(choices=AccountType, default=constants.AccountType.CUSTOMER)
    password = StringField(null=True)
    first_name = StringField(required=True, max_length=100)
    last_name = StringField(required=True, max_length=100)
    user_status = StringField(choices=UserStatus, default=constants.UserStatus.PENDING)
    status = StringField(choices=UserAccountStatus, default=constants.UserAccountStatus.ACTIVE)
    password_reset_on_next_login = BooleanField(default=False)
    account_modified_by = StringField(max_length=100, default='')
    terms_accepted = BooleanField(default=False)
    last_login_at = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.utcnow)
    modified_at = DateTimeField()
    meta = {'collection': 'UserAccount'}
