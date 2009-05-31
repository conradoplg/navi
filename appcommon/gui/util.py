from functools import wraps


def freeze(fn):
    @wraps(fn)
    def wrapped_fn(self, *args, **kwargs):
        self.Freeze()
        try:
            fn(self, *args, **kwargs)
        finally:
            self.Thaw()
    return wrapped_fn