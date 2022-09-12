from trame.ui.html import DivLayout


def initialize(server):
    state = server.state
    state.grid_options.append("empty")

    with DivLayout(server, template_name="empty") as layout:
        layout.root.add_child("Some empty content...")
