class DDResolver:
    def __init__(self):
        pass

    def __str__(self):
        return self.description

    def process(self, identity):
        print("Processing identity: "+str(identity))
