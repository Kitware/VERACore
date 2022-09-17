r"""
Define your classes and create the instances that you need to expose
"""
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class MyBusinessLogic:
    def __init__(self, server):
        self._server = server


# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------


def initialize(server):
    engine = MyBusinessLogic(server)
    return engine
