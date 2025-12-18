# Core exceptions


class CoreError(Exception):
    pass


class ValidationError(CoreError):
    pass


class StorageError(CoreError):
    pass
