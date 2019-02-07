from functools import wraps

import inflection
from flask import g


def gcache(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if hasattr(g, f.__name__):
            return getattr(g, f.__name__)
        else:
            value = f(*args, **kwargs)
            setattr(g, f.__name__, value)
            return value

    return wrapper


def camel_to_snake(f):
    @wraps(f)
    def wrapper(self, data):
        snake_case_data = {
            inflection.underscore(key): value for key, value in data.items()
        }
        return f(self, snake_case_data)

    return wrapper
