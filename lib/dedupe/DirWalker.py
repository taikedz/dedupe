"""
Directory Walker
"""

import os
import logging

import ddexceptions as DDE

global log
log = logging.Logger("dedupe")

log.info("information")
log.warning("a warning")

class DirWalker:

    def __init__(self, top_dir, handlers):
        """
        top_dir - str: the path of the topmost directory
        handlers - dict(str: Event --> DDHandler: handler instance)
        """
        self.top_dir = top_dir
        self.handlers = handlers
        self.file_stack = [top_dir]
        self.walking = False

        log.debug("Created a walker on <%s>" % (top_dir))

    def walk(self):
        """ An iterative breadth-first walker, for triggering relevant events appropriately.
        """
        if not self.walking:
            self.walking = True
        else:
            raise DDE.WalkerException("Tried to call walker twice")

        while len(self.file_stack) > 0:
            current_item = self.pop()
            log.debug("Processing <%s> : <%s>" % (self.top_dir, current_item.getPath()) )

            try:
                if current_item.isdir():
                    self.__processEvent("EVT_ENCOUNTER_DIR", current_item)

                    # If we get past the encounter, we *intend* to enter at this point
                    #  trigger this event before placing things on the file stack
                    self.__processEvent("EVT_ENTER_DIR", current_item)

                    # "Effectively" enter
                    log.debug("Entering <%s>." %(current_item.getName()) )

                    dir_contents = current_item.getContents()
                    log.debug("%i items: %s" % (len(dir_contents), str(dir_contents)) )

                    # Ensure each path is added with a full path
                    self.file_stack[0:0] = [current_item.getFullPath() + child_path for chidl_path in dir_contents]
                    log.debug("File stack now has %i items to process." % (len(self.file_stack)))
                else:
                    self.__processEvent("EVT_ENCOUNTER_FILE", current_item)

            except DDE.ProcessorSkipException as e:
                log.info(str(e))
                pass

    def __processEvent(self, event_name, current_item):
        log.debug("Event [%s] :: %s" % (event_name, current_item.getName()) )
        for handler in self.handlers[event_name]:
            handler.process(current_item)

    def __pop(self):
        return WalkerItem(self.remove() , self.top_dir)

class WalkerItem:
    """ Convenience filesystem node representation

    Tracks metadata relevant to the walk
    """

    def __init__(self, path, top_dir):
        self.path = path
        self.top_dir = top_dir

    def getTopDirPath(self):
        return self.top_dir

    def getFullPath(self):
        return self.path

    def getName(self):
        return os.path.basename(self.path)

    def getContents(self):
        """ Get a listing of files and folders in the folder this WalkerItem represents

        The list is sorted by byte value.
        """
        contents = os.listdir(self.path)
        contents.sort()
        return contents

    def isdir(self):
        return os.path.isdir(self.path)

    def islink(self):
        return os.path.islink(self.path)
