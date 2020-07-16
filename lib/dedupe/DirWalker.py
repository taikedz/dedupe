"""
Directory Walker
"""

import os
import ddlog

import ddexceptions as DDE
import WalkerItem
import Handlers

log = ddlog.getLogger("dedupe")

class DirWalker:

    def __init__(self, top_dir):
        """
        top_dir - str: the path of the topmost directory
        """
        self.top_dir = top_dir
        self.file_stack = [top_dir]
        self.walking = False

        log.debug("Created a walker on <%s>" % (top_dir))

    def walk(self):
        """ An iterative walker, for triggering relevant events appropriately.

        The walker will trigger the following events, causing their handlers to be run:
        - EVT_ENTER_DIR - when entering a directory, before adding its contents to the walk stack for processing
        - EVT_ENCOUNTER_DIR - when a directory is found, before processing it
        - EVT_ENCOUNTER_FILE - when a file is found, before processing it
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
                    Handlers.processEvent(Handlers.EVT_ENCOUNTER_DIR, current_item)

                    # If we get past the encounter, we *intend* to enter at this point
                    #  trigger this event before placing things on the file stack
                    Handlers.processEvent(Handlers.EVT_ENTER_DIR, current_item)

                    # "Effectively" enter
                    log.debug("Entering <%s>." %(current_item.getName()) )

                    dir_contents = current_item.getContents()
                    log.debug("%i items: %s" % (len(dir_contents), str(dir_contents)) )

                    # Ensure each path is added with a full path
                    self.file_stack[0:0] = ["%s%s%s" % (current_item.getFullPath(), os.path.sep, child_path) for child_path in dir_contents]
                    log.debug("File stack now has %i items to process." % (len(self.file_stack)))
                else:
                    Handlers.processEvent(Handlers.EVT_ENCOUNTER_FILE, current_item)

            except DDE.ProcessorSkipException as e:
                log.info(str(e))
                pass

    def __pop(self):
        """ Returns a WalkerItem of the topmost item on the file stack. Removes that item from the stack.
        """
        return WalkerItem.WalkerItem(self.file_stack.pop(0) , self.top_dir)
