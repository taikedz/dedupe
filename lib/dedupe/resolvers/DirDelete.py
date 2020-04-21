import GenericResolver as gr

class DirDeleteResolver(gr.DDResolver):
    def __init__(self):
        self.description = "Select instances, delete parent directories"


def getResolverInstance():
    return DirDeleteResolver()
