class CoreError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args
        self.message = None

    def __str__(self):
        if self.message:
            return self.message
        return "Connection Error"
