'''

This module contains all the datastore models for the website's datastore.

Created on Oct 10, 2014
@author: rockwotj
'''
from google.appengine.ext import ndb

FILE_TYPES = ["Exam 1", "Exam 2", "Exam 3", "Exam 4", "Exam 5", "Final", "Quiz", "Homework"]

DEPARTMENTS = ['AB', 'BE', 'BIO', 'CE', 'CHE', 'CHEM', 'CSSE', 'ECE', 'EM', 'EMGT', 'EP', 'IA', 'SV', 'GS', 'ES', 'MA', 'ME', 'OE', 'PH']

class File(ndb.Model):
    department = ndb.StringProperty(required=True, choices=DEPARTMENTS)
    classNumber = ndb.IntegerProperty(required=True)
    professor = ndb.StringProperty(required=True)
    fileType = ndb.StringProperty(required=True, choices=FILE_TYPES)
    TermCode = ndb.IntegerProperty(required=True)  # 201510 is FallQtr for the 2014-2015 school year


