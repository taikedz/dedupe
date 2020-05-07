"""
Directory Walker
"""

import os
import logging

import ddexceptions as DDE

log = logging.getLogger("dedupe")

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
        """ An iterative walker, for triggering relevant events appropriately.

        The walker will trigger the following events, causing their handlers to be run:
        - DirWalker.EVT_ENTER_DIR - when entering a directory, before adding its contents to the walk stack for processing
        - DirWalker.EVT_ENCOUNTER_DIR - when a directory is found, before processing it
        - DirWalker.EVT_ENCOUNTER_FILE - when a file is found, before processing it
        """
        if not self.walking:
            self.walking = True
        else:
            raise DDE.WalkerException("Tried to call walker twice")

        while len(self.file_stack) > 0:
            current_item = self.__pop()
            log.debug("Processing <%s> : <%s>" % (self.top_dir, current_item.getFullPath()) )

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
                    self.file_stack[0:0] = ["%s%s%s" % (current_item.getFullPath(), os.path.sep, child_path) for child_path in dir_contents]
                    log.debug("File stack now has %i items to process." % (len(self.file_stack)))
                else:
                    self.__processEvent("EVT_ENCOUNTER_FILE", current_item)

            except DDE.ProcessorSkipException as e:
                log.info(str(e))
                pass

    def __processEvent(self, event_name, current_item):
        """ Runs the handlers associated with the named event. If the handler returns a message, logs the message.
        """
        log.debug("Event [%s] :: %s" % (event_name, current_item.getName()) )
        for handler in self.handlers[event_name]:
            result = handler.process(current_item)
            if result != None:
                log.info(str(result) )

    def __pop(self):
        """ Returns a WalkerItem of the topmost item on the file stack. Removes that item from the stack.
        """
        return WalkerItem(self.file_stack.pop(0) , self.top_dir)

class WalkerItem:
    """ Convenience filesystem node representation

    Tracks metadata relevant to the walk
    """

    def __init__(self, path, top_dir):
        if not os.path.exists(path):
            raise FileNotFoundError("<%s> does not exist" % path)

        self.path = path
        self.top_dir = top_dir

    def __str__(self):
        return self.getFullPath()

    def getTopDirPath(self):
        """ Return the path of the top directory being processed
        """
        return self.top_dir

    def getFullPath(self):
        """ Get the path name of the file, with the path from the top directory.
        """
        return self.path

    def getName(self):
        """ Get the file name of the current item, without its leading path
        """
        return os.path.basename(self.path)

    def getContents(self, full_paths=False):
        """ Get a listing of files and folders in the folder this WalkerItem represents

        The list is sorted by byte value.

        If full_paths is True, prefixes all content names with the full path of the current item
        """
        contents = os.listdir(self.path)
        contents.sort()
        
        if full_paths:
            contents = ["%s%s%s" % (self.getFullPath(), os.path.sep, child_path) for child_path in contents]

        return contents

    def isdir(self):
        """ Returns True if the item is a directory
        """
        return os.path.isdir(self.path)

    def islink(self):
        """ Returns True if the item is a symlink
        """
        return os.path.islink(self.path)
