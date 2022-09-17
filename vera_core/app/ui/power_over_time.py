import plotly.express as px

from trame.ui.html import DivLayout
from trame.widgets import plotly


OPTION = {
    "name": "power_over_time",
    "label": "Power Over Time",
    "icon": "mdi-chart-line",
}


def create_line(vera_out_file, indices=(0, 0, 0, 0)):
    exposures = [x.exposure[0] for x in vera_out_file.states]
    pin_powers = [x.pin_powers[indices] for x in vera_out_file.states]

    kwargs = {
        "x": exposures,
        "y": pin_powers,
        "labels": {
            "x": "exposure",
            "y": "pin_powers",
        },
    }
    return px.line(**kwargs)


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller
    state.grid_options.append(OPTION)

    @state.change("selected_assembly", "selected_layer", "selected_i", "selected_j")
    def on_cell_change(
        selected_assembly, selected_layer, selected_i, selected_j, **kwargs
    ):
        indices = (selected_j, selected_i, selected_layer, selected_assembly)
        indices = tuple(map(int, indices))
        ctrl.update_power_over_time(create_line(vera_out_file, indices))

    with DivLayout(server, template_name="power_over_time") as layout:
        layout.root.style = "height: 100%; width: 100%;"

        style = "; ".join(
            [
                "width: 100%",
                "height: 100%",
                "user-select: none",
            ]
        )
        figure = plotly.Figure(
            display_logo=False,
            display_mode_bar=False,
            style=style,
            # selected=(on_event, "["selected", utils.safe($event)]"),
            # hover=(on_event, "["hover", utils.safe($event)]"),
            # selecting=(on_event, "["selecting", $event]"),
            # unhover=(on_event, "["unhover", $event]"),
        )
        ctrl.update_power_over_time = figure.update
