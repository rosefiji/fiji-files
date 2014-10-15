'''

This module contains all the datastore models for the website's datastore.

Created on Oct 10, 2014
@author: rockwotj
'''
from google.appengine.ext import ndb

class File(ndb.Model):
    department = ndb.StringProperty()
    classNumber = ndb.StringProperty()
    professor = ndb.StringProperty()
    fileType = ndb.StringProperty()
    # Valid Types:
    #    Exam 1 - 5
    #    Final
    #    Quiz
    #    Homework
    TermCode = ndb.IntegerProperty()
    # 201510 is FallQtr for the 2014-2015 school year

class ScholarshipCommittee(ndb.Model):
    emails = ndb.StringProperty(repeated=True)
