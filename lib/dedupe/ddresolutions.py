import importlib

import ddbaseutils

RESOLVERS = [
    "FileDelete",
    "DirDelete",
    "DirMerge",
    "Skip",
]

class DDResolutions:

    def __init__(self, resolvers=RESOLVERS, path="resolvers"):
        """Arguments:

        resolvers - a list of resolver names (optional)
        path - the path along which to find the resolvers (optional)
        """
        self.resolvers = []
        for r in resolvers:
            resolverfile = "%s.%s" % (path,r)
            mod = importlib.import_module(resolverfile)
            self.resolvers.append( mod.getResolverInstance() )

    def getUserResolver(self, identity, default_selection=None):
        # Pass a single identity that needs resolving.
        # Get action descriptions from resolvers, offer a choice
        # Pass control to selected resolver

        identity.showPaths() # User needs to know what they are resolving
        resolver = ddbaseutils.getUserSelection("Resolve by", self.resolvers, default=default_selection)
        return resolver
