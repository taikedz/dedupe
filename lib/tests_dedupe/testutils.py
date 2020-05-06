import os
import shutil

base_path = "/tmp/test-dedupe"

def touch(path, data=None):
    path = "%s/%s" % (base_path, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
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

