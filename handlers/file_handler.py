"""
This module contains the handlers for all file uploads and takes care of uploading the files to the old FIJI files site
and returning the new information to the the datastore.

Created on Oct 10, 2014.
Written by: rockwotj.
"""
import gdata.sites.client


def upload_file(rosefiji_email, password, dept, file_handle):
    departments = ['AB', 'BE', 'BIO', 'CE', 'CHE', 'CHEM', 'CSSE', 'ECE', 'EM', 'EMGT', 'EP', 'IA', 'SV', 'GS', 'ES', 'MA', 'ME', 'OE', 'PH']
    if dept not in departments:
        raise Exception("Invalid Department")
    client = gdata.sites.client.SitesClient(source='rhophi-fijifiles-v1', site='fiji-files', domain='rosefiji.com')
    # Authenticate using your Google email address and password.
    client.ClientLogin(rosefiji_email, password, client.source)
    # http://gdata-python-client.googlecode.com/hg/pydocs/gdata.sites.client.html
    uri = '%s?kind=%s&path=/%s' % (client.MakeContentFeedUri(), 'filecabinet', dept)
    feed = client.GetContentFeed(uri=uri)
    # MediaSource?
    entry = client.upload_attachment(file_handle, feed.entry[0], content_type='application/pdf', title="Test File", description="Uploaded from Python!")
    return entry.GetAlternateLink().href


