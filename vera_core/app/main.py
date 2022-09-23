from functools import partial

from trame.app import get_server, dev

from . import ui
from .core.vera_out_file import VeraOutFile


def _reload(vera_out_file):
    server = get_server()
    dev.reload(ui)
    ui.initialize(server, vera_out_file)


def main(server=None, **kwargs):

    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    server.cli.add_argument(
        "--data",
        help="Data file to load",
        dest="data_file",
        required=True,
    )
    args, _ = server.cli.parse_known_args()
    data_file = args.data_file

    vera_out_file = VeraOutFile(data_file)

    f = partial(_reload, vera_out_file=vera_out_file)

    # Make UI auto reload
    server.controller.on_server_reload.add(f)

    # Init application
    ui.initialize(server, vera_out_file)

    # Start server
    server.start(**kwargs)


if __name__ == "__main__":
    main()
