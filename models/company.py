from datetime import datetime

from mongoengine import *
import constants

import constants
MONGO_URI = constants.MONGO_URI
connect(host=MONGO_URI)
CompanyStatus = (constants.CompanyStatus.DISABLED, constants.CompanyStatus.ACTIVE)


class Company(Document):
    company_id = StringField(unique=True, required=True)
    email = StringField(required=True, max_length=100)
    company_name = StringField(required=True, max_length=100)
    country_region = StringField(required=True, max_length=10)
    registration_status = StringField(choices=constants.ModelChoices.REGISTRATION_STATUS_CHOICES,
                                      default=constants.RegistrationStatus.PENDING)
    business_address = StringField(default='')
    billing_address = StringField(default='')
    billing_contact = StringField(default='', max_length=50)
    legal_contact = StringField(default='', max_length=50)
    status = StringField(choices=CompanyStatus, default=constants.CompanyStatus.ACTIVE)
    created_at = DateTimeField(default=datetime.utcnow)
    modified_at = DateTimeField()
    meta = {'collection': 'Company'}
