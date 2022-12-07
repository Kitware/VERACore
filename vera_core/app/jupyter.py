from trame.app import get_server, jupyter
from vera_core.app import ui

from .core.vera_out_file import VeraOutFile


def show(data=None, server=None, **kwargs):
    """Run and display the trame application in jupyter's event loop

    The kwargs are forwarded to IPython.display.IFrame()
    """
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    vera_out_file = VeraOutFile(data)

    # Initialize app
    ui.initialize(server, vera_out_file)

    # Show as cell result
    jupyter.show(server, **kwargs)


def jupyter_proxy_info():
    """Get the config to run the trame application via jupyter's server proxy

    This is provided to the `jupyter_serverproxy_servers` entrypoint, and the
    jupyter server proxy will use it to start the application as a separate
    process.
    """
    return {
        "command": ["vera-core", "-p", "0", "--server"],
    }
