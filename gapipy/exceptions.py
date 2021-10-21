
class GapipyException(Exception):
    pass


class EmptyPartialUpdateException(GapipyException):
    def __str__(self):
        return "gapipy computed no changes for partial update"
