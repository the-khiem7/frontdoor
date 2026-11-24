"""The frontdoor harness: the design board, the renderer and the browser daemon behind the `fd` command."""

VERSION = "0.1.0"


class FdError(Exception):
    """An expected failure: printed as one line on stderr, exit code 1 (or the code given)."""

    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code
