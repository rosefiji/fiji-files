'''

This module contains all the datastore models for the website's datastore.

Created on Oct 10, 2014
@author: rockwotj
'''
from google.appengine.api import memcache
from google.appengine.ext import ndb
from collections import OrderedDict


FILE_TYPES = ["Exam1", "Exam2", "Exam3", "Exam4", "Exam5", "Final", "Quiz", "Homework", "Paper", "Other"]

DEPARTMENTS = ['BE', 'BIO', 'CE', 'CHE', 'CHEM', 'CSSE', 'ECE', 'EM', 'EMGT', 'EP', 'IA', 'SV', 'GS', 'ES', 'MA', 'ME', 'OE', 'PH']

DEPARTMENT_NAMES = OrderedDict([('BE', "Biomedical Engineering"),
                    ('BIO', "Biology"),
                    ('CE', "Civil Engineering"),
                    ('CHE', "Chemical Engineering"),
                    ('CHEM', "Chemistry"),
                    ('CSSE', "Computer Science & Software Engineering"),
                    ('ECE', "Electrical & Computer Engineering"),
                    ('EM', "Engineering Mechanics"),
                    ('EMGT', "Engineering Management"),
                    ('EP', "Engineering Physics"),
                    ('ES', "Sophomore Engineering"),
                    ('GS', "Global Science"),
                    ('IA', "Ideas & Arts"),
                    ('MA', "Mathematics"),
                    ('ME', "Mechanical Engineering"),
                    ('OE', "Optical Engineering"),
                    ('PH', "Physics"),
                    ('SV', "Society & Values"),
                    ('IV', "Interview Preperation") ])

class Course(ndb.Model):
    # Includes a key with an id of dept and num? ie. CSSE120
    department = ndb.StringProperty(required=True, choices=DEPARTMENTS)
    course_number = ndb.IntegerProperty(required=True, choices=range(101, 600))

class File(ndb.Model):
    # Randomly generated key?
    # course = ndb.KeyProperty(required=True, kind=Course) PARENT KEY!
    professor = ndb.StringProperty(required=True)
    file_type = ndb.StringProperty(required=True, choices=FILE_TYPES)
    termcode = ndb.IntegerProperty(required=True)  # 201510 is FallQtr for the 2014-2015 school year
    url = ndb.StringProperty(required=True)  # This is the link to the pdf file
    delete_url = ndb.StringProperty(required=True)
    comments = ndb.TextProperty()

    def get_string_termcode(self):
        term = str(self.termcode)
        year = int(term[:-2])
        qtr = int(term[-2:])
        year = str(year - 1) + "-" + str(year)
        if qtr == 10:
            qtr = "Fall "
        elif qtr == 20:
            qtr = "Winter "
        elif qtr == 30:
            qtr = "Spring "
        elif qtr == 40:
            qtr = "Summer "
        return qtr + year


class UploadCount(ndb.Model):
    count = ndb.IntegerProperty(default=0)


def get_upload_number():
    client = memcache.Client()
    entity = client.get('COUNT')
    if not entity:
        # if not in cache go to datastore
        entity = UploadCount.get_by_id("COUNT")
        if not entity:
            # not in datastore create a new count
            entity = UploadCount(id="COUNT")
    entity.count += 1
    client.set('COUNT', entity)
    entity.put()
    return "%08d" % entity.count
