from trame.ui.html import DivLayout

OPTION = {
    "name": "top_quadrant",
    "label": "Top Quadrant",
    "icon": "mdi-chart-donut-variant",
}


def initialize(server):
    state = server.state
    state.grid_options.append(OPTION)

    with DivLayout(server, template_name="top_quadrant") as layout:
        layout.root.add_child("Some top_quadrant content...")
