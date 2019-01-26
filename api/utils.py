import functools

from flask import g


def gcache(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if hasattr(g, f.__name__):
            return getattr(g, f.__name__)
        else:
            value = f(*args, **kwargs)
            setattr(g, f.__name__, value)
            return value

    return wrapper
