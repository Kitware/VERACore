import plotly.express as px

from trame.ui.html import DivLayout
from trame.widgets import plotly


OPTION = {
    "name": "time_plot",
    "label": "Time Plot",
    "icon": "mdi-chart-line",
}


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    def create_line(selected_array, indices=(0, 0, 0, 0)):
        exposures = [x.exposure[0] for x in vera_out_file.states]

        if selected_array == "pin_volumes":
            # It's just going to be a flat line. The volumes don't change.
            pin_volumes = vera_out_file.core.pin_volumes
            array = [pin_volumes[indices] for _ in vera_out_file.states]
        else:
            array = [getattr(x, selected_array)[indices] for x in vera_out_file.states]

        kwargs = {
            "x": exposures,
            "y": array,
            "labels": {
                "x": "exposure",
                "y": selected_array,
            },
        }
        figure = px.line(**kwargs)
        figure.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        return figure

    @state.change(
        "selected_array",
        "selected_assembly",
        "selected_layer",
        "selected_i",
        "selected_j",
    )
    def on_cell_change(
        selected_array,
        selected_assembly,
        selected_layer,
        selected_i,
        selected_j,
        **kwargs
    ):
        indices = (selected_j, selected_i, selected_layer, selected_assembly)
        indices = tuple(map(int, indices))
        ctrl.update_time_plot(create_line(selected_array, indices))

    with DivLayout(server, template_name="time_plot") as layout:
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
        ctrl.update_time_plot = figure.update
