import logging

logger = logging.getLogger("uvicorn")


class Singleton(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # initiate cls by calling original cls.__call__ method
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Abandoned decorator version of singleton lol,
# class Singleton(object):
#
#     def __init__(self, decorated: Callable):
#         if not isinstance(decorated, Callable):
#             raise TypeError("Decorated object must be callable")
#
#         self.decorated = decorated()
#         self._instance = None
#
#     def instance(self) -> object:
#         if not self._instance:
#             self._instance = self.decorated
#         return self._instance
#
#     def __call__(self):
#         raise TypeError("Singleton object must be called with instance")
#
#     def __isinstance__(self, inst: any):
#         return isinstance(self.decorated, inst)
