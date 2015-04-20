from Report import Report

__author__ = 'Rohan'

# User class - sets up the functionalities of the User member


class User:
    # Initialize user class with fields: name, reports, starred reports, and groups
    def __init__(self, name):
        self.name = name
        self.reports = []
        self.starred = []
        self.groups = []

    # Add a report to the starred array - a report has been starred
    def starreport(self, report):
        self.starred.append(report)

    # Add a new report to the user's list of reports
    def addreport(self, author, short_description, long_description, title="Title", private=False, date_of_event=None,
                  location=None, keywords=None, files=None):
        newreport = Report(author, short_description, long_description, title, private, date_of_event, location,
                           keywords, files)
        self.reports.append(newreport)

    # def editreport(self):