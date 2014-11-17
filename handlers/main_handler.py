import json

import webapp2

import main, models


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = main.jinja_env.get_template("templates/index.html")
        self.response.out.write(template.render())

class FileDepartmentHandler(webapp2.RequestHandler):
    def get(self, dept):
        template = main.jinja_env.get_template("templates/main.html")
        values = {"dept" : dept, "depts" : models.DEPARTMENTS, "dept_names": models.DEPARTMENT_NAMES}
        self.response.out.write(template.render(values))

class FileCourseHandler(webapp2.RequestHandler):
    def get(self, dept, course_number):
        pass

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
        """ Displays a list of all files in the datastore """
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
        self.response.headers['Content-Type'] = 'application/json'
        response = {}
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
        self.response.out.write(json.dumps(response))

    def verify_access(self):
        return True

SITEMAP = [ ("/", MainHandler),
            (r"/files/(\w+)", FileDepartmentHandler),
            (r"/files/(\w+)/(\d+)", FileCourseHandler) ]

API = [ (r"/datastore", FileDatastoreHandler) ]
