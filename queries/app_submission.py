import datetime
import logging
import traceback

import constants
from models.app_submission import AppSubmission
from serializers.app_submission import serialize_app_submission
from queries.app import AppQueries
from serializers.serializer_utils import serialize_before_save


class AppSubmissionQueries():
    def __init__(self):
        self.model = AppSubmission

    def get_by_id(self, submission_id):
        try:
            submission = self.model.objects.get(id=submission_id)
            return serialize_app_submission(submission)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def insert_one(self, data):
        try:
            insert_obj = serialize_before_save(data)
            logging.exception(f"**insert_obj {insert_obj}")
            submission = self.model.objects.insert(AppSubmission(**insert_obj))
            app_collection = AppQueries()
            app_collection.update_one(submission['app_id'], {'modified_at': datetime.datetime.utcnow()})
            return serialize_app_submission(submission)
        except Exception as e:
            logging.exception(e)
            logging.exception(str(traceback.format_exc()))
            return None

    def update_one(self, submission_id, data):
        try:
            if submission_id:
                update_obj = serialize_before_save(data)
                submission_obj = self.model.objects(id=submission_id).modify(**update_obj, new=True)
                if submission_obj:
                    submission_obj = serialize_app_submission(submission_obj)
                    app_collection = AppQueries()
                    app_collection.update_one(submission_obj['app_id'], {'modified_at': datetime.datetime.utcnow()})
                return submission_obj
            else:
                return False
        except Exception as e:
            logging.exception("Error while updating submission - {}".format(str(e)))
            return False

    def get_submissions_by_pkg_name(self, pkg_name, sort_by):
        try:
            submissions = self.model.objects(app_pkg_name=pkg_name).order_by(sort_by)
            return serialize_app_submission(submissions)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_un_archived_submissions_by_pkg_name(self, pkg_name, sort_by):
        try:
            submissions = self.model.objects(app_pkg_name=pkg_name,
                                             submission_state__ne=constants.SubmissionStates.ARCHIVED).\
                order_by(sort_by)
            return serialize_app_submission(submissions)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_submissions_by_app_id(self, app_id, sort_order=None):
        try:
            if sort_order:
                submissions = self.model.objects(app_id=app_id).order_by(*sort_order)
            else:
                submissions = self.model.objects(app_id=app_id)
            return serialize_app_submission(submissions)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_submissions_by_app_id_and_states(self, app_id, submission_states, sort_order=None):
        try:
            if sort_order:
                submissions = self.model.objects(app_id=app_id, submission_state__in=submission_states).\
                    order_by(*sort_order)
            else:
                submissions = self.model.objects(app_id=app_id, submission_state__in=submission_states)
            return serialize_app_submission(submissions)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_app_ids_by_submission_states(self, submission_states):
        try:
            req_fields = ['app_id']
            submissions = serialize_app_submission(self.model.objects(submission_state__in=submission_states).
                                                   only(*req_fields))
            app_ids = [submission['app_id'] for submission in submissions]
            return list(set(app_ids))
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_app_ids_by_modified_by(self, modified_by):
        try:
            req_fields = ['app_id']
            submissions = serialize_app_submission(self.model.objects(last_updated_by__icontains=modified_by).
                                                   only(*req_fields))
            app_ids = [submission['app_id'] for submission in submissions]
            return list(set(app_ids))
        except Exception:
            logging.exception(traceback.format_exc())
            return None


    def get_many_submissions_by_app_ids(self, app_ids):
        try:
            submissions = self.model.objects(app_id__in=app_ids)
            return serialize_app_submission(submissions)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_submissions_grouped_by_state_for_apps_ids(self, app_ids):
        try:
            submissions = self.model.objects.aggregate([
                {
                    '$match': {
                        'app_id': {'$in': app_ids}
                    }
                },
                {
                    '$group': {
                        '_id': '$app_id',
                        'data': {
                            '$push': {
                                'state': '$submission_state',
                                'submission_id': '$_id',
                                'submission_type': '$submission_type',
                                'modified_at': '$modified_at',
                                'last_updated_by': '$last_updated_by'
                            }
                        }
                    }
                }
            ])
            submissions_dict = {item['_id']: item for item in list(submissions)}
            return submissions_dict
        except Exception:
            logging.exception(traceback.format_exc())
            return {}

    def get_submissions_by_pkg_name_and_state(self, pkg_name, submission_state, sort_order=None):
        try:
            if sort_order:
                submissions = self.model.objects(app_pkg_name=pkg_name, submission_state=submission_state)\
                    .order_by(*sort_order)
            else:
                submissions = self.model.objects(app_pkg_name=pkg_name, submission_state=submission_state)
            return serialize_app_submission(submissions)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def get_submissions_by_app_id_and_state(self, app_id, submission_state, sort_order=None):
        try:
            if sort_order:
                submissions = self.model.objects(app_id=app_id, submission_state=submission_state).order_by(*sort_order)
            else:
                submissions = self.model.objects(app_id=app_id, submission_state=submission_state)
            return serialize_app_submission(submissions)
        except Exception:
            logging.exception(traceback.format_exc())
            return None

    def delete_submissions_by_ids(self, app_ids):
        try:
            return self.model.objects(app_id__in=app_ids).delete(), True
        except Exception:
            logging.exception(traceback.format_exc())
            return 0, False
