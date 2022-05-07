
class UnsupportedFileTypeException(Exception):
    def __init__(self, *args):
        self.message = 'Unsupported file type extension'
        if args:
            self.message += (': ' + str(args[0]))

    def __str__(self):
        return self.message
