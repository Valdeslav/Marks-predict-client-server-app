
class UnsupportedFileTypeException(Exception):
    def __str__(self, *args):
        self.message = 'Unsupported file type extension'
        if args:
            self.message += (': ' + args[0])

    def __str__(self):
        return self.message
