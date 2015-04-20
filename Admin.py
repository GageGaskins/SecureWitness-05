from Report import Report

__author__ = 'Rohan'

# Admin class is same as User class; however, admin user can:
# promote other users to admin status, add users to groups, ...


class Admin:
    # initialize an admin user class with fields: name, reports, starred reports, and groups
    def __init__(self, name):
        self.name = name
        self.reports = []
        self.starred = []
        self.groups = []

    # allows admin user to star certain reports
    def starreport(self, report):
        self.starred.append(report)

    # user can add a report to their reports array
    def addreport(self, author, short_description, long_description, title="Title", private=False, date_of_event=None,
                  location=None, keywords=None, files=None):
        newreport = Report(author, short_description, long_description, title, private, date_of_event, location,
                           keywords, files)
        self.reports.append(newreport)

    # admin user can add users to groups
    def addtogroup(self, groupname, users):
        for user in users:
            user.groups.append(groupname)