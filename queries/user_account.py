import logging
import traceback

from mongoengine import DoesNotExist

import constants
from models.user_account import UserAccount
from serializers.serializer_utils import serialize_before_save
from serializers.user_account import serialize_user_account


class UserAccountQueries:
    def __init__(self):
        self.model = UserAccount

    def insert_one(self, data):
        try:
            insert_obj = serialize_before_save(data)
            user_obj = self.model(**insert_obj)
            return serialize_user_account(user_obj.save())
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_user_by_email(self, email):
        try:
            user_obj = self.model.objects.get(email=email)
            return serialize_user_account(user_obj)
        except DoesNotExist:
            return None
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_all_emails_associated_with_company_id(self, company_id, account_type=None):
        try:
            company_id = str(company_id)
            developer_emails = []
            sales_emails = []
            if account_type == constants.AccountType.CUSTOMER:
                user = self.model.objects(company_ids__contains=company_id, account_type=constants.AccountType.CUSTOMER)
            elif account_type == constants.AccountType.SALES_REP:
                user = self.model.objects(company_ids__contains=company_id,
                                          account_type=constants.AccountType.SALES_REP)
            else:
                user = self.model.objects(company_ids__contains=company_id)
            if user:
                user_obj = serialize_user_account(user)
                for user in user_obj:
                    if user['account_type'] == constants.AccountType.SALES_REP:
                        sales_emails.append(user.get("email"))
                    elif user['account_type'] == constants.AccountType.CUSTOMER:
                        developer_emails.append(user.get("email"))
            return developer_emails, sales_emails
        except Exception:
            logging.exception(traceback.format_exc())
            return None, None

    def update_one(self, email, data):
        try:
            if email:
                update_obj = serialize_before_save(data)
                user_obj = self.model.objects(email=email).modify(**update_obj, new=True)
                if user_obj:
                    user_obj = serialize_user_account(user_obj)
                    return user_obj
            return False
        except Exception as e:
            print(e)
            logging.exception(traceback.format_exc())
            return False

    def get_all_users_by_user_status(self, user_status, sort_order=None):
        try:
            if sort_order:
                users = self.model.objects(user_status__in=user_status).order_by(*sort_order)
            else:
                users = self.model.objects(user_status__in=user_status)
            return serialize_user_account(users)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_paginated_user_list(self, sort_order=None, page=None, limit=None):
        try:
            if sort_order:
                users = self.model.objects(status__ne=constants.CompanyStatus.DISABLED).order_by(*sort_order)
            else:
                users = self.model.objects(status__ne=constants.CompanyStatus.DISABLED)

            if page and limit:
                limit = int(limit)
                offset = (page - 1) * limit
                users = users.skip(offset).limit(limit)

            count_of_users = users.count()

            return serialize_user_account(users), count_of_users
        except Exception:
            logging.exception(traceback.format_exc())
            return [], 0

    def get_users_by_emails(self, emails):
        try:
            users = self.model.objects(email__in=emails)
            return serialize_user_account(users) if users else []
        except Exception:
            logging.exception(traceback.format_exc())
            return []

    def validate_user_email_company(self, email, company_id):
        # Driver method defined in utils.py for this function
        try:
            user = self.get_user_by_email(email)
            user_companies = user.get('company_ids')
            if user_companies and company_id in user_companies:
                return True
            else:
                return False
        except Exception:
            logging.exception(traceback.format_exc())
            return False

    def get_email_ids_by_first_name(self, first_name):
        try:
            req_fields = ['email']
            user_accounts = self.model.objects(status__ne=constants.UserAccountStatus.DISABLED,
                                               first_name__icontains=first_name).only(*req_fields)
            user_account_list = serialize_user_account(user_accounts) if user_accounts else []
            email_ids = [user_account['email'] for user_account in user_account_list]
            return list(set(email_ids))
        except Exception:
            logging.exception(traceback.format_exc())
            return []

    def get_email_ids_by_last_name(self, last_name):
        try:
            req_fields = ['email']
            user_accounts = self.model.objects(status__ne=constants.UserAccountStatus.DISABLED,
                                               last_name__icontains=last_name).only(*req_fields)
            user_account_list = serialize_user_account(user_accounts) if user_accounts else []
            email_ids = [user_account['email'] for user_account in user_account_list]
            return list(set(email_ids))
        except Exception:
            logging.exception(traceback.format_exc())
            return []

    def get_non_terms_accepted_users(self):
        try:
            users = self.model.objects(terms_accepted__ne=True)
            return serialize_user_account(users)
        except Exception:
            logging.exception(traceback.format_exc())
            return None
