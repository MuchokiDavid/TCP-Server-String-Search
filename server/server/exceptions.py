"""
Defines custom exceptions for handling specific error cases in the server.
"""


class InvalidPayloadError(Exception):
    """
    Exception raised when the payload is invalid.
    """
    def __init__(self, message="Invalid payload"):
        self.message = message
        super().__init__(self.message)

class SearchFileReadError(Exception):
    """
    Exception raised when there is an error reading the search file.
    """
    pass

class FileAccessError(Exception):
    """
    Exception raised when there is an error accessing the file.
    """
    pass
