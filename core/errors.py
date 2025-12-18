"""Core exceptions (Phase 1)."""


class CoreError(Exception):
    pass


class ValidationError(CoreError):
    pass


class StorageError(CoreError):
    pass
