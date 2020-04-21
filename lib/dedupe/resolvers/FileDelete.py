import GenericResolver as gr

class FileDeleteResolver(gr.DDResolver):
    def __init__(self):
        self.description = "Select files to delete"


def getResolverInstance():
    return FileDeleteResolver()
