import datetime

__author__ = 'Jackie Shrader'


class Report:

    def __init__(self, author, short_description, long_description, title="Title", private=False, date_of_event=None, location=None, keywords=None, files=None):
        # necessary characteristics
        self.author = author
        self.title = title
        self.private = private
        self.timestamp = datetime.datetime.now()
        self.short_description = short_description
        self.long_description = long_description
        # optional functionality
        self.date_of_event = None or date_of_event
        self.location = None or location
        self.keywords = None or keywords
        self.files = None or files

    def __repr__(self):
        return self.author + ", " + self.title + ", " + self.short_description + ", " + self.long_description

def main():
    test = Report("Jackie", "Small Test", "This is the first test of the report object", "Test", False)
    print(test)
    print(test.timestamp)

main()

