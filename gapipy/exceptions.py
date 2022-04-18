"""gapipy exception types"""


class GapipyException(Exception):
    """Generic base-class for all gapipy exception-types."""


class EmptyPartialUpdateError(ValueError, GapipyException):
    """A partial update of a resource was requested, but no data has changed."""
    def __init__(self, *args):
        """Initialize with a default message if the caller hasn't supplied anything."""
        if not args:
            args = ("gapipy computed no changes for partial update",)

        super(EmptyPartialUpdateError, self).__init__(*args)
