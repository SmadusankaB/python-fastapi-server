class CustomException(Exception):
    """
    A class used to represent a CustomException
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        # add more propeeties as needed
        Exception.__init__(self, status_code)  # make status_code mandatory
