import logging
import traceback
import datetime
import re
from mongoengine import DoesNotExist

from mongoengine.queryset.visitor import Q

import constants
from models.app import App
from serializers.app import serialize_app
from serializers.serializer_utils import serialize_before_save


class AppQueries():
    def __init__(self):
        self.model = App

    def get_app_by_app_pkg(self, app_pkg):
        try:
            app = self.model.objects.get(app_pkg_name__iexact=app_pkg)
            return serialize_app(app)
        except DoesNotExist:
            return None
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_app_by_id(self, app_id):
        try:
            app = self.model.objects.get(id=app_id)
            return serialize_app(app)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_apps_by_app_ids(self, app_ids):
        try:
            apps = self.model.objects.filter(app_id__in=app_ids)
            return serialize_app(apps)
        except Exception:
            logging.exception(traceback.format_exc())
            return []

    def get_apps_by_ids(self, ids):
        try:
            apps = self.model.objects.filter(id__in=ids)
            return serialize_app(apps)
        except Exception:
            logging.exception(traceback.format_exc())
            return []

    def get_company_id_from_app_obj_id(self, app_id):
        try:
            app = self.model.objects.get(id=app_id)
            app_obj = serialize_app(app)
            company_id = app_obj.get("company_id")
            return company_id
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_company_id_from_app_id(self, app_id):
        try:
            app = self.model.objects.get(app_id=app_id)
            app_obj = serialize_app(app)
            company_id = app_obj.get("company_id")
            return company_id
        except Exception:
            logging.error(traceback.format_exc())
            return None

    def get_all_used_tags(self):
        try:
            req_fields = ['tags']
            tags = []
            apps = serialize_app(self.model.objects().only(*req_fields))
            for app in apps:

                app_tags = app.get('tags', [])
                if app_tags:
                    tags.extend(app_tags)
            return set(tags)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def insert_one(self, data):
        try:
            insert_obj = serialize_before_save(data)
            app = self.model.objects.insert(App(**insert_obj))
            return serialize_app(app)

        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def filter_apps_base_query(self, base_query, filter_key, filter_value):
        if filter_key == 'app_id':
            return base_query.filter(app_id__icontains=filter_value)
        elif filter_key == 'app_title':
            return base_query.filter(app_title__en__icontains=filter_value)
        elif filter_key == 'app_pkg_name':
            return base_query.filter(app_pkg_name__icontains=filter_value)
        elif filter_key == 'tier':
            return base_query.filter(tier__in=filter_value)
        elif filter_key == 'tags':
            tags = "|".join([f'^{tag}$' for tag in filter_value])
            tags_regex = re.compile(tags)
            return base_query.filter(tags=tags_regex)
        elif filter_key == 'iap_integration':
            return base_query.filter(iap_integration__in=filter_value)
        elif filter_key == 'login_integration':
            return base_query.filter(login_integration__in=filter_value)
        elif filter_key == 'nft_integration':
            return base_query.filter(nft_integration__in=filter_value)
        elif filter_key == 'developer_name':
            from queries.company import CompanyQueries
            company_ids = CompanyQueries().get_company_ids_by_name(filter_value)
            return base_query.filter(company_id__in=company_ids)
        elif filter_key == 'modified_by':
            from queries.app_submission import AppSubmissionQueries
            app_ids = AppSubmissionQueries().get_app_ids_by_modified_by(modified_by=filter_value)
            return base_query.filter(id__in=app_ids)
        elif filter_key == 'submission_states':
            from queries.app_submission import AppSubmissionQueries
            app_ids = AppSubmissionQueries().get_app_ids_by_submission_states(submission_states=filter_value)
            return base_query.filter(id__in=app_ids)
        elif filter_key == 'modified_at_range':
            # 2021-12-21_2022-02-21
            start_date, end_date = filter_value.split("_")
            modified_start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            modified_end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            span = datetime.timedelta(hours=24)
            modified_end = modified_end_date + span
            return base_query.filter(modified_at__gte=modified_start, modified_at__lte=modified_end)
        else:
            return base_query

    def get_filtered_apps(self, sort_order=None, page=None, limit=None, filters=None):
        try:
            base_query = self.model.objects(status__ne=constants.AppStatus.DISABLED)
            if filters:
                for filter_key, filter_value in filters.items():
                    base_query = self.filter_apps_base_query(base_query, filter_key, filter_value)
            if sort_order:
                base_query = base_query.order_by(*sort_order)
            if page and limit:
                offset = (int(page) - 1) * int(limit)
                base_query = base_query.skip(offset).limit(int(limit))

            count_of_apps = base_query.count()
            return serialize_app(base_query), count_of_apps
        except Exception:
            logging.exception(traceback.format_exc())
            return [], 0

    def get_apps(self, sort_order=None, page=None, limit=None, search=None, company_id=None):
        try:
            if company_id:
                base_query = self.model.objects(status__ne=constants.AppStatus.DISABLED).filter(company_id=company_id)
            else:
                base_query = self.model.objects(status__ne=constants.AppStatus.DISABLED)

            if search:
                base_query = base_query.filter(Q(app_title__en__icontains=search) | Q(app_pkg_name__icontains=search))
            if sort_order:
                base_query = base_query.order_by(*sort_order)
            if page and limit:
                offset = (int(page) - 1) * int(limit)
                base_query = base_query.skip(offset).limit(int(limit))

            count_of_apps = base_query.count()
            return serialize_app(base_query), count_of_apps
        except Exception:
            logging.exception(traceback.format_exc())
            return [], 0

    def get_iap_app_id_from_id(self, id):
        try:
            app = self.model.objects.get(id=id)
            app_obj = serialize_app(app)
            iap_app_id = app_obj.get("app_id", None)
            return iap_app_id
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def update_one(self, app_id, data):
        try:
            if app_id:
                update_obj = serialize_before_save(data)
                return self.model.objects(id=app_id).update(**update_obj)
            else:
                return False
        except Exception as e:
            logging.exception("Error while updating app - {}".format(str(e)))
            return False

    def get_all_app_pkg_names(self):
        try:
            req_fields = ['app_pkg_name']
            pkg_names = []
            apps = serialize_app(self.model.objects().only(*req_fields))
            for app in apps:
                pkg_name = app.get('app_pkg_name')
                if pkg_name:
                    pkg_names.append(pkg_name)
            return pkg_names
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_all_iap_integrated_apps(self):
        try:
            # Todo -> Check if the filter needs to inserted object or filter method
            iap_integrated_apps = self.model.objects().filter(iap_integration=True)
            serialized_apps = serialize_app(iap_integrated_apps)
            return serialized_apps
        except Exception:
            logging.error(traceback.format_exc())

    def delete_apps_by_ids(self, app_ids):
        try:
            return self.model.objects(id__in=app_ids).delete(), True
        except Exception:
            logging.exception(traceback.format_exc())
            return 0, False

    def get_all_apps_partial_info(self):
        try:
            req_fields = ['company_id', 'app_id', 'app_pkg_name']
            apps = serialize_app(self.model.objects().only(*req_fields))
            apps_info = dict()
            for app in apps:
                apps_info[app.get('app_pkg_name')] = {
                    'company_id': app.get('company_id'),
                    'app_id': app.get('app_id'),
                    'app_pkg_name': app.get('app_pkg_name')
                }
            return apps_info
        except Exception:
            logging.error(traceback.format_exc())
            return []
