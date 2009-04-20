from collections import Iterable

def flattened_chain(iterables):
    for it in iterables:
        if isinstance(it, Iterable):
            for elem in flattened_chain(it):
                yield elem
        else:
            yield it

def flattened_full_chain(iterables):
    for it in iterables:
        if isinstance(it, Iterable):
            yield it
            for elem in flattened_full_chain(it):
                yield elem
        else:
            yield it