import json

from google.appengine.ext import ndb
import webapp2

import models


class FileDatastoreHandler(webapp2.RequestHandler):
    """ The RESTful API calls for the file manager to use """

    API_PROXY = "sdaemon@rosefiji.com"

    API_PASSCODE = ""

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
        response = json.loads(self.request.get("data"))
        self.response.out.write(json.dumps(response))

    def post(self):
        """ Adds a file to the datastore. """
        if not self.verify_access():
            self.response.out.write(FileDatastoreHandler.ERROR_PAGE)
            self.response.set_status(401)
            return
        file_request = json.loads(self.request.body)
        self.response.headers['Content-Type'] = 'application/json'
        response = {}
        try:
            course_dept = file_request["department"]
            course_number = file_request["courseNumber"]
            course_key = ndb.Key(id=course_dept + course_number)
            if not course_key.get():
                models.Course(key=course_key,
                              department=course_dept,
                            course_number=course_number).put()
            file_to_add = models.File(parent=course_key,
                                      professor=file_request["professor"],
                                      file_type=file_request["type"],
                                      termcode=file_request["termcode"],
                                      file_url=file_request["href"],
                                      file_delete_url=file_request["deleteLink"],
                                      comments=file_request["comments"])
            file_to_add.put()
            response["upload_request"] = "success"
        except:
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
        response = {"delete_request" :  "success"}
        self.response.out.write(json.dumps(response))

    def verify_access(self):
        self.request.cookies.get('user')
        self.request.cookies.get('passcode')
        return True

API = [ ("/datastore", FileDatastoreHandler) ]
