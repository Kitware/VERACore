from trame.ui.html import DivLayout

OPTION = {
    "name": "power_over_time",
    "label": "Power Over Time",
    "icon": "mdi-chart-line",
}


def initialize(server):
    state = server.state
    state.grid_options.append(OPTION)

    with DivLayout(server, template_name="power_over_time") as layout:
        layout.root.add_child("Some power_over_time content...")
