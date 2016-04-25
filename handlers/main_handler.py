import webapp2
import logging
import main, models
from models import Course, File
import gdata.gauth
import gdata.sites.client
import gdata.docs.service
import gdata.data
import json
from datetime import date
from oauth2client.client import SignedJwtAssertionCredentials
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = main.jinja_env.get_template("templates/index.html")
        values = {"departments": models.DEPARTMENT_NAMES}
        self.response.out.write(template.render(values))

class FileDepartmentHandler(webapp2.RequestHandler):
    def get(self, dept):
        template = main.jinja_env.get_template("templates/main.html")
        values = {"departments": models.DEPARTMENT_NAMES, "types": models.FILE_TYPES}
        values["dept"] = dept
        termcodes = []
        this_year = date.today().year + 1
        this_month = date.today().month
        for year in range(this_year, this_year - 3, -1):
            yearcode = year * 100
            for quarter, value in [('Spring', 30), ("Winter", 20), ("Fall", 10)]:
                termcodes.append({"term":quarter + " " + str(year - 1) + "-" + str(year) ,"code":yearcode + value})
        values["termcodes"] = termcodes
        if 1 <= this_month <= 2:
            # Winter Quarter
            values["termcodes"] = termcodes[4:]
        elif 3 <= this_month <= 6:
            # Spring Quarter
            values["termcodes"] = termcodes[3:]
        elif 7 <= this_month <= 8:
            # Summer
            pass
        elif 9 <= this_month <= 11:
            # Fall Quarter
            values["termcodes"] = termcodes[2:]
        elif this_month == 12:
            # Winter Quarter
            values["termcodes"] = termcodes[1:]
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

class DeleteFileHandler(webapp2.RequestHandler):
    def post(self):
        scope = 'https://sites.google.com/feeds/'
        client = gdata.sites.client.SitesClient(source='rosefiji-fijifiles-v1', site='fiji-files', domain='rosefiji.com')
        with open('credentials.json') as jsonfile:
            jsondata = json.load(jsonfile)
            credentials = SignedJwtAssertionCredentials(
                jsondata['client_email'],
                jsondata['private_key'],
                scope=scope,
                sub='trockwood@rosefiji.com'
            )
        auth2token = gdata.gauth.OAuth2TokenFromCredentials(credentials)
        auth2token.authorize(client)
        delete_key = self.request.get('delete_key')
        try:
            urlfetch.set_default_fetch_deadline(30)
            client.Delete(delete_key, force=True)
        except Exception, e:
            pass
        files = models.File.query(models.File.delete_url == delete_key)
        ndb.delete_multi([key for key in files.iter(keys_only=True)])
        self.redirect(self.request.referer)

class EditFileHandler(webapp2.RequestHandler):
    def post(self):
        key = ndb.Key(urlsafe=self.request.get('entity_key'))
        file_type = self.request.get('type')
        termcode = self.request.get('term')
        comments = self.request.get('comments')
        prof = self.request.get('professor')
        f = key.get()
        f.termcode = int(termcode)
        f.file_type = file_type
        f.comments = comments
        f.professor = prof
        f.put()
        self.redirect(self.request.referer)

class FileCourseHandler(webapp2.RequestHandler):
    def get(self, dept, course_number):
        pass

class UploadHandler(webapp2.RequestHandler):

    def getSize(self,fileobject):
        fileobject.seek(0,2) # move the cursor to the end of the file
        size = fileobject.tell()
        return size

    def get(self):
       template = main.jinja_env.get_template("templates/upload.html")
       values = {"departments": models.DEPARTMENT_NAMES, "depts": models.DEPARTMENTS, "types": models.FILE_TYPES}
       termcodes = []
       this_year = date.today().year + 1
       this_month = date.today().month
       for year in range(this_year, this_year - 3, -1):
           yearcode = year * 100
           for quarter, value in [('Spring', 30), ("Winter", 20), ("Fall", 10)]:
               termcodes.append({"term":quarter + " " + str(year - 1) + "-" + str(year) ,"code":yearcode + value})
       values["termcodes"] = termcodes
       if 1 <= this_month <= 2:
           # Winter Quarter
           values["termcodes"] = termcodes[4:]
       elif 3 <= this_month <= 6:
           # Spring Quarter
           values["termcodes"] = termcodes[3:]
       elif 7 <= this_month <= 8:
           # Summer
           pass
       elif 9 <= this_month <= 11:
           # Fall Quarter
           values["termcodes"] = termcodes[2:]
       elif this_month == 12:
           # Winter Quarter
           values["termcodes"] = termcodes[1:]
       hash = self.request.params.get('msg')
       if hash:
           if hash == 'success':
               values['msg'] = 'Congrats! The file was uploaded. The chapter applauds your committment to academic success.'
           elif hash == 'retry':
               values['msg'] = 'The file needs to be less than 10MB or the request was bad. Please try submitting again, or shrinking the file down.'
           elif hash == 'error':
               values['msg'] = 'Error uploading file! Please contact Tech if this is a problem'
       self.response.out.write(template.render(values))


    def post(self):
       scope = 'https://sites.google.com/feeds/'
       client = gdata.sites.client.SitesClient(source='rosefiji-fijifiles-v1', site='fiji-files', domain='rosefiji.com')
       with open('credentials.json') as jsonfile:
            jsondata = json.load(jsonfile)
            credentials = SignedJwtAssertionCredentials(
                     jsondata['client_email'],
                     jsondata['private_key'],
                     scope=scope,
                     sub='trockwood@rosefiji.com'
            )
       auth2token = gdata.gauth.OAuth2TokenFromCredentials(credentials)
       auth2token.authorize(client)
       dept = self.request.params.get('department')
       file_id = models.get_upload_number()
       uri = '%s?kind=%s' % (client.MakeContentFeedUri(),'filecabinet&path=/' + dept)
       feed = client.GetContentFeed(uri=uri)
       f = self.request.params.get('file')
       ext = f.filename.split(".")[-1].upper()
       media = gdata.data.MediaSource(file_handle=f.file.read(),
           content_type=gdata.docs.service.SUPPORTED_FILETYPES.get(ext) or 'application/octet-stream',
           content_length=self.getSize(self.request.params.get('file').file))
       try:
           urlfetch.set_default_fetch_deadline(30)
           attachment = client.UploadAttachment(media, feed.entry[0], title=file_id, description='UPLOADED TO NEW FIJI FILES SITE')
       except Exception, e:
           logging.exception(e)
           self.redirect('/upload?msg=retry')
           return
       try:
           course_dept = dept
           course_number = int(self.request.params.get("courseNumber"))
           course_key = ndb.Key("Course", course_dept + str(course_number))
           course = course_key.get()
           if not course:
               course = models.Course(key=course_key,
                             department=course_dept,
                             course_number=course_number)
               course.put()
           file_to_add = models.File(parent=course_key,
                                     professor=self.request.params.get("professor"),
                                     file_type=self.request.params.get("type"),
                                     termcode=int(self.request.params.get("termcode")),
                                     url="https://sites.google.com/a/rosefiji.com/fiji-files/" + dept + "/" + file_id,
                                     delete_url=str(attachment.get_edit_link().href),
                                     comments=self.request.params.get("comments"))
           file_to_add.put()
           self.redirect('/upload?msg=success')
       except Exception, e:
           logging.exception(e)
           self.redirect('/upload?msg=error')

SITEMAP = [ ("/", MainHandler),
            ("/upload", UploadHandler),
            ("/delete", DeleteFileHandler),
            ("/edit", EditFileHandler),
            (r"/(\w+)", FileDepartmentHandler),
            (r"/(\w+)/(\d+)", FileCourseHandler) ]
