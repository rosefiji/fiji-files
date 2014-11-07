import webapp2

import main

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = main.jinja_env.get_template("templates/index.html")
        self.response.out.write(template.render())

class FileDepartmentHandler(webapp2.RequestHandler):
    def get(self, dept):
        pass

class FileCourseHandler(webapp2.RequestHandler):
    def get(self, dept, course_number):
        pass

class FileDatastoreHandler(webapp2.RequestHandler):
    def get(self):
        """ Displays a list of all files in the datastore """
        pass

    def post(self):
        """ Adds a file to the datastore. """
        pass

    def delete(self):
        """ Removes a file from the data store. """
        pass

SITEMAP = [("/", MainHandler), (r"/files/(\w+)", FileDepartmentHandler), (r"/files/(/w+)/(/d+)", FileCourseHandler)]
