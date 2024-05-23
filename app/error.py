from flask import Flask, jsonify, current_app


class FlaskBaseError(Exception):
    """
    application base error, use this error, you can define the response code & message
    """

    status_code = 500

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """
        convert to dict
        """
        return {
            "error_type": self.__class__.__name__,
            "error": self.message,
            "code": self.status_code
        }


class ParameterError(FlaskBaseError):
    """
    parameter related error
    """

    status_code = 400


class ParameterLostError(ParameterError):
    """
    parameter lost error
    """

    def __init__(self, param_name):
        ParameterError.__init__(self, f"{param_name} must be provided.")


def set_error_handler():
    """
    set flask app error handler
    """
    @current_app.errorhandler(Exception)
    def handle_invalid_usage(e: Exception):
        """
        handle invalid message
        """

        if isinstance(e, FlaskBaseError):
            response = jsonify(e.to_dict())
            response.status_code = e.status_code
            return response

        status_code = 500  # default error status code
        error = str(e)  # default error message

        if hasattr(e, "code"):
            status_code = e.code
        elif hasattr(e, "status_code"):
            status_code = e.status_code

        if hasattr(e, "message"):
            error = e.message
        elif hasattr(e, "description"):
            error = e.description

        response = jsonify({
            "code": status_code,
            "error_type": e.__class__.__name__,
            "error": error,
        })

        response.status_code = status_code
        return response
