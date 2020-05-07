import ddexceptions as DDE

def process(current_item):
    if current_item.islink():
        raise ProcessorSkipException("Skip %s" %(current_item))
