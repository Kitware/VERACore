from trame.ui.html import DivLayout


def initialize(server):
    state = server.state
    state.grid_options.append("power_over_time")

    with DivLayout(server, template_name="power_over_time") as layout:
        layout.root.add_child("Some power_over_time content...")
