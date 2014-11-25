import json
import logging

from google.appengine.ext import ndb
import webapp2

import models


API_PROXY = "sdaemon@rosefiji.com"

API_PASSCODE = ""

class FileDatastoreHandler(webapp2.RequestHandler):
    """ The RESTful API calls for the file manager to use """

    ERROR_PAGE = """<html><head>
                    <title>401 Authorization Required</title>
                    </head><body>
                    <h1>Authorization Required</h1>
                    <p>This server could not verify that you
                    are authorized to access the data
                    requested. This url is for API calls only.
                    Do not try to make calls in your browser. </p>
                    <hr>
                    <address>fiji-files site</address>
                    </body></html>"""

    def get(self):
        """ Displays a list of all files in the datastore for a dept"""
        if not self.verify_access():
            self.response.out.write(FileDatastoreHandler.ERROR_PAGE)
            self.response.set_status(401)
            return
        self.response.headers['Content-Type'] = 'application/json'
        response = []
        dept = self.request.get("dept")
        course_keys = models.Course.query(models.Course.department == dept)
        for course_key in course_keys.iter(keys_only=True):
            files = models.File.query(ancestor=course_key)
            course = course_key.get()
            for f in files:
                data = {}
                data["department"] = course.department
                data["courseNumber"] = course.course_number
                data["professor"] = f.professor
                data["type"] = f.file_type
                data["termcode"] = f.termcode
                data["href"] = f.url
                data["deleteLink"] = f.delete_url
                data["comments"] = f.comments
                response.append(data)
        self.response.out.write(json.dumps(response))

    def post(self):
        """ Adds a file to the datastore. """
        if not self.verify_access():
            self.response.out.write(FileDatastoreHandler.ERROR_PAGE)
            self.response.set_status(401)
            return
        file_request = json.loads(self.request.get('uploadRequest'))
        logging.info(file_request)
        self.response.headers['Content-Type'] = 'application/json'
        response = {}
        try:
            course_dept = file_request["department"]
            course_number = file_request["courseNumber"]
            course_key = ndb.Key("Course", course_dept + str(course_number))
            course = course_key.get()
            if not course:
                course = models.Course(key=course_key,
                              department=course_dept,
                              course_number=course_number)
                course.put()
            file_to_add = models.File(parent=course_key,
                                      professor=file_request["professor"],
                                      file_type=file_request["type"],
                                      termcode=file_request["termcode"],
                                      url=file_request["href"],
                                      delete_url=file_request["deleteLink"],
                                      comments=file_request["comments"])
            file_to_add.put()
            response["upload_request"] = "success"
        except Exception, e:
            logging.exception(e)
            response["upload_request"] = "failure"
        self.response.out.write(json.dumps(response))

    def put(self):
        """ Gets the number of files in the datastore """
        if not self.verify_access():
            self.response.out.write(FileDatastoreHandler.ERROR_PAGE)
            self.response.set_status(401)
            return
        self.response.headers['Content-Type'] = 'application/json'
        response = {"count" : models.get_upload_number()}
        self.response.out.write(json.dumps(response))

    def delete(self):
        """ Removes a file from the data store. """
        if not self.verify_access():
            self.response.out.write(FileDatastoreHandler.ERROR_PAGE)
            self.response.set_status(401)
            return
        self.response.headers['Content-Type'] = 'application/json'
        response = {}
        delete_type = self.request.get("deleteRequest")
        delete_key = self.request.get("deleteKey")
        if delete_type == "file" and delete_key:
            files = models.File.query(models.File.delete_url == delete_key)
            ndb.delete_multi([key for key in files.iter(keys_only=True)])
            response["delete_request"] = "success"
        elif delete_type == "course" and delete_key:
            course_key = ndb.Key("Course", delete_key)
            files = models.File.query(ancestor=course_key)
            ndb.delete_multi([key for key in files.iter(keys_only=True)])
            course_key.delete()
            response["delete_request"] = "success"
        else:
            response["delete_request"] = "fail"
        self.response.out.write(json.dumps(response))

    def verify_access(self):
        user = self.request.cookies.get('user')
        passcode = self.request.cookies.get('passcode')
        return user == API_PROXY and passcode == API_PASSCODE

API = [ ("/datastore", FileDatastoreHandler) ]
