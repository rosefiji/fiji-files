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

SITEMAP = [ ("/", MainHandler),
            (r"/files/(\w+)", FileDepartmentHandler),
            (r"/files/(\w+)/(\d+)", FileCourseHandler) ]
