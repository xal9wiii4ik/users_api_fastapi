from starlette.requests import Request


def get_db(request: Request):
    """ Get current state of db """

    return request.state.db
