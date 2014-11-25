import webapp2

import main, models
from models import Course, File


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = main.jinja_env.get_template("templates/index.html")
        values = {"departments": models.DEPARTMENT_NAMES}
        self.response.out.write(template.render(values))

class FileDepartmentHandler(webapp2.RequestHandler):
    def get(self, dept):
        template = main.jinja_env.get_template("templates/main.html")
        values = {"departments": models.DEPARTMENT_NAMES}
        values["dept"] = dept
        course_keys = Course.query(Course.department == dept)
        courses = []
        files = {}
        for course_key in course_keys.iter(keys_only=True):
            courses.append(course_key.string_id())
            files[course_key.string_id()] = File.query(ancestor=course_key)
        courses.sort()
        values["courses"] = courses
        values["files"] = files
        self.response.out.write(template.render(values))

class FileCourseHandler(webapp2.RequestHandler):
    def get(self, dept, course_number):
        pass

SITEMAP = [ ("/", MainHandler),
            (r"/(\w+)", FileDepartmentHandler),
            (r"/(\w+)/(\d+)", FileCourseHandler) ]
