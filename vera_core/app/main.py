from trame.app import get_server, dev

from . import engine, ui
from .core.vera_out_file import VeraOutFile


def _reload():
    server = get_server()
    dev.reload(ui)
    ui.initialize(server)


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

    # Make UI auto reload
    server.controller.on_server_reload.add(_reload)

    # Init application
    engine.initialize(server)
    ui.initialize(server, vera_out_file)

    # Start server
    server.start(**kwargs)


if __name__ == "__main__":
    main()
