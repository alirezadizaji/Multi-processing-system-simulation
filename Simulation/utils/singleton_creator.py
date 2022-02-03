
def singleton_creator(obj: object):    
    """ a decorator modifying a python class into singleton object """

    instance = [None]

    def wrapper(*args, **kwargs):

        if instance[0] is None:
            instance[0] = obj(*args, **kwargs)
        
        return instance[0]

    return wrapper