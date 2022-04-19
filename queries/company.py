import datetime
import logging
import traceback

from mongoengine import DoesNotExist

import constants
from models.company import Company
from serializers.company import serialize_company
from serializers.serializer_utils import serialize_before_save


class CompanyQueries():
    def __init__(self):
        self.model = Company

    def get_or_insert(self, company_data):
        try:
            company_id = company_data.get('company_id')
            if company_id:
                try:
                    company = self.model.objects.get(company_id=company_id)
                    logging.info(f"company exists {company_id}")
                    return serialize_company(company)
                except DoesNotExist:
                    insert_obj = serialize_before_save(company_data)
                    inserted_company = self.model.objects.insert(Company(**insert_obj))
                    return serialize_company(inserted_company)
            else:
                logging.exception("Company - company_id missing")
                return None
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def update_one(self, company_id, data):
        try:
            if company_id:
                update_obj = serialize_before_save(data)
                company = self.model.objects(company_id=company_id).modify(**update_obj, new=True)
                return serialize_company(company)
            else:
                return False
        except Exception as e:
            logging.exception("Error while updating company - {}".format(str(e)))
            return False

    def get_company_by_id(self, company_id):
        try:
            company = self.model.objects.get(company_id=company_id)
            return serialize_company(company)
        except DoesNotExist:
            return None
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_paginated_companies_by_registration_status(self, registration_status_list, sort_order=None,
                                                       page=None, limit=None):
        try:
            if sort_order:
                companies = self.model.objects(registration_status__in=registration_status_list,
                                               status__ne=constants.CompanyStatus.DISABLED).order_by(*sort_order)
            else:
                companies = self.model.objects(registration_status__in=registration_status_list,
                                               status__ne=constants.CompanyStatus.DISABLED)
            if page and limit:
                offset = (page - 1) * limit
                companies = companies.skip(offset).limit(limit)

            count_of_companies = companies.count()
            return serialize_company(companies), count_of_companies
        except Exception:
            logging.exception(traceback.format_exc())
            return [], 0

    def get_companies_by_ids(self, company_ids, sort_order=None):
        try:
            if company_ids:
                if sort_order:
                    companies = self.model.objects(status__ne=constants.CompanyStatus.DISABLED,
                                                   company_id__in=company_ids).order_by(*sort_order)
                else:
                    companies = self.model.objects(status__ne=constants.CompanyStatus.DISABLED,
                                                   company_id__in=company_ids)
                return serialize_company(companies)
            else:
                logging.exception(
                    f"company_ids not passed in get_companies_by_ids")
                return []
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_company_ids_by_name(self, company_name):
        try:
            req_fields = ['company_id']
            companies = serialize_company(self.model.objects(status__ne=constants.CompanyStatus.DISABLED,
                                                             company_name__icontains=company_name).only(*req_fields))
            company_ids = [company['company_id'] for company in companies]
            return list(set(company_ids))
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_paginated_company_list(self, sort_order, page=None, limit=None):
        try:
            companies = self.model.objects(
                status__ne=constants.CompanyStatus.DISABLED).order_by(*sort_order)
            if page and limit:
                offset = (page - 1) * limit
                companies = companies.skip(offset).limit(limit)

            count_of_companies = companies.count()
            return serialize_company(companies), count_of_companies
        except Exception:
            logging.exception(traceback.format_exc())
            return [], 0

    def filter_companies_base_query(self, base_query, filter_key, filter_value):
        if filter_key == 'company_id':
            return base_query.filter(company_id__icontains=filter_value)
        elif filter_key == 'company_name':
            return base_query.filter(company_name__icontains=filter_value)
        elif filter_key == 'email':
            return base_query.filter(email__icontains=filter_value)
        elif filter_key == 'country_region':
            return base_query.filter(country_region__icontains=filter_value)
        elif filter_key == 'registration_status':
            return base_query.filter(registration_status__in=filter_value)
        elif filter_key == 'created_at_range':
            start_date, end_date = filter_value.split("_")
            created_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            created_end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            span = datetime.timedelta(hours=24)
            created_end = created_end_date + span
            return base_query.filter(created_at__gte=created_start, created_at__lte=created_end)
        elif filter_key == 'first_name':
            from queries.user_account import UserAccountQueries
            email_ids = UserAccountQueries().get_email_ids_by_first_name(filter_value)
            return base_query.filter(email__in=email_ids)
        elif filter_key == 'last_name':
            from queries.user_account import UserAccountQueries
            email_ids = UserAccountQueries().get_email_ids_by_last_name(filter_value)
            return base_query.filter(email__in=email_ids)
        else:
            return base_query

    def get_filtered_companies(self, sort_order=None, page=None, limit=None, filters=None):
        try:
            base_query = self.model.objects(status__ne=constants.CompanyStatus.DISABLED)
            if filters:
                for filter_key, filter_value in filters.items():
                    base_query = self.filter_companies_base_query(base_query, filter_key, filter_value)
            if sort_order:
                base_query = base_query.order_by(*sort_order)
            if page and limit:
                offset = (page - 1) * limit
                base_query = base_query.skip(offset).limit(limit)

            count_of_companies = base_query.count()
            if count_of_companies:
                return serialize_company(base_query), count_of_companies
            else:
                return [], 0
        except Exception:
            logging.exception(traceback.format_exc())
            return [], 0

    def get_all_companies_partial_info(self):
        try:
            req_fields = ['company_id', 'email', 'company_name', 'country_region']
            companies = serialize_company(self.model.objects().only(*req_fields))
            companies_info = dict()
            for company in companies:
                companies_info[company.get('email')] = {
                    'company_id': company.get('company_id'),
                    'email': company.get('email'),
                    'company_name': company.get('company_name'),
                    'country_region': company.get('country_region')
                }
            return companies_info
        except Exception:
            logging.error(traceback.format_exc())
            return []
