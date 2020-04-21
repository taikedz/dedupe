import GenericResolver as gr

class SkipResolver(gr.DDResolver):
    def __init__(self):
        self.description = "(skip, do nothing)"

    def process(self):
        print("Skipping")


def getResolverInstance():
    return SkipResolver()
