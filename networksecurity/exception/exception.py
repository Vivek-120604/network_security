import sys
from networksecurity.logging.logger import logging

def error_message_detail(error, error_detail:sys):
    try:
        _, _, exc_tb = error_detail.exc_info()
        if exc_tb is None:
            # Get the caller's frame if no active exception
            frame = sys._getframe(1)
            file_name = frame.f_code.co_filename
            line_number = frame.f_lineno
        else:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
    except:
        file_name = "Unknown"
        line_number = 0
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, line_number, str(error)
    )
    return error_message

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        logging.error(NetworkSecurityException(e, sys))
        raise NetworkSecurityException(e, sys)
