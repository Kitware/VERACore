from trame.ui.html import DivLayout


def initialize(server):
    state = server.state
    state.grid_options.append("top_quadrant")

    with DivLayout(server, template_name="top_quadrant") as layout:
        layout.root.add_child("Some top_quadrant content...")
