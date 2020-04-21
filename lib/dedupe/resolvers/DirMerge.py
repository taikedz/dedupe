import GenericResolver as gr

class DirMergeResolver(gr.DDResolver):
    def __init__(self):
        self.description = "Select a target file's parent directory, merge other directories to the target directory"


def getResolverInstance():
    return DirMergeResolver()
