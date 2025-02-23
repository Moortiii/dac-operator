class ResourceNotFoundException(Exception):
    """
    An exception that indicates that we attempted to fetch a resource using the
    kubernetes API, but were unable to find it.
    """

    ...


class ResourceValidationError(Exception):
    """
    An exception that indicates if we attempted to convert a resource response into a
    Pydantic model, and failed to do so.
    """

    ...
