import logging

import webapp2

from models import Course
from models import File


class CleanDataStore(webapp2.RequestHandler):
    def get(self):
        logging.info("Starting to clean the datastore")
        courses = Course.query()
        for key in courses.iter(keys_only=True):
            files = File.query(ancestor=key)
            if files.get() is None:
                key.delete()
                logging.info("Deleting: " + key.string_id())
        logging.info("Done cleaning the datastore")

CRON = [("/tasks", CleanDataStore)]
