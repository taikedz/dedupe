class DbApiGeneric:
    def __init__(self, *args, **kwargs):
        if type(self) == DbApiGeneric:
            raise NotImplementedError("Cannot call init of DbApiGeneric. Please instantiate from a subclass.")


    def add_path(self, path, size, short_hash, full_hash):
        raise NotImplementedError()


    def delete_path(self, path):
        raise NotImplementedError()


    def update_path(self, path, size, short_hash, full_hash):
        raise NotImplementedError()


    def find_path_duplicates(self, path):
        raise NotImplementedError()


    def find_hash_duplicates(self, full_hash):
        raise NotImplementedError()
