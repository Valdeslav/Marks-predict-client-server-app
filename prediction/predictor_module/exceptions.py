class EmptyListOfSubjectsWithMark(Exception):
    def __init__(self, *args):
        self.message = 'There is no students with mark in this subject'
        if args:
            self.message += (': ' + str(args[0]))

    def __str__(self):
        return self.message
