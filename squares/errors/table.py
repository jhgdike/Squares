from . import BaseError


class BusyError(BaseError):
    pass


class JoinTableError(BaseError):
    pass


class StartError(BaseError):
    pass


class OutRangeError(BaseError):
    pass


class TakeError(BaseError):
    pass
