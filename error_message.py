import warnings

class DuplicateWarning(UserWarning):
    """ Warning class when duplicate label values are detected """
    pass

class SaveError(Exception):
    """ Error message when save function is run and there is no bounding box in the JSON """
    pass

class DefaultBoxWarning(UserWarning):
    """ Warning message if save function is run before CreateJSON function"""
    pass

class ReplaceWarning(UserWarning):
    """ Warning message if template folder is already present """
    pass
