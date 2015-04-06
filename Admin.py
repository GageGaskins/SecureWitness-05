from Report import Report

__author__ = 'Rohan'


class Admin:
    def __init__(self, name):
        self.name = name
        self.reports = []
        self.starred = []
        self.groups = []

    def starreport(self, report):
        self.starred.append(report)

    def addreport(self, author, short_description, long_description, title="Title", private=False, date_of_event=None,
                  location=None, keywords=None, files=None):
        newreport = Report(author, short_description, long_description, title, private, date_of_event, location,
                           keywords, files)
        self.reports.append(newreport)

    def addtogroup(self, groupname, users):
        for user in users:
            user.groups.append(groupname)