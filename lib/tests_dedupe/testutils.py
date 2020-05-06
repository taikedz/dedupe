import os
import shutil

######
# Test result store
# For use in global access

result_store = {}

def store(name, value):
    result_store[name] = value

def retrieve(name):
    return result_store[name]

#######
# Filesystem mocking

base_path = "/tmp/test-dedupe"

def touch(path, data=None, symlink_source=None):
    path = "%s/%s" % (base_path, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if symlink_source:
        symlink_source = "%s/%s" % (base_path, symlink_source)
        os.symlink(symlink_source, path, target_is_directory=os.path.isdir(symlink_source))
    else:
        fh = open(path, 'w')
        if data != None:
            fh.write(data)
        fh.close()

def getPath(path=None):
    if path == None:
        path = ""
    path = "%s/%s" % (base_path, path)
    path = os.path.abspath(path)
    return path

def removeTmp():
    shutil.rmtree(base_path)

