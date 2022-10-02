import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from trame.ui.html import DivLayout
from trame.widgets import plotly


OPTION = {
    "name": "axial_plot",
    "label": "Axial Plot",
    "icon": "mdi-align-horizontal-center",
}


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    def create_line(selected_array, indices=(0, 0, 0, 0)):
        selected_j, selected_i, selected_layer, selected_assembly = indices

        full_array = vera_out_file.array(selected_array)
        array = full_array[selected_j, selected_i, :, selected_assembly]

        kwargs = {
            "x": array,
            "y": vera_out_file.core.axial_mesh_means,
            "labels": {
                "x": selected_array,
                "y": "Axial (cm)",
            },
        }
        figure = px.line(**kwargs)

        # Add a horizontal line indicating our current axial position
        # # FIXME: why is add_hline only plotting from x==0 to x==1?
        # kwargs = {
        #     "y": vera_out_file.core.axial_mesh_means[selected_layer],
        #     "line_dash": "dash",
        #     "line_color": "red",
        # }
        # figure.add_hline(**kwargs)
        #
        # # Because the above won't work, we have to make it manually
        float_info = np.finfo(np.float64)
        kwargs = {
            "x": [float_info.min, float_info.max],
            "y": [vera_out_file.core.axial_mesh_means[selected_layer]] * 2,
            "mode": "lines",
            "line": go.scatter.Line(color="red", dash="dash"),
            "showlegend": False,
        }
        figure.add_trace(go.Scatter(**kwargs))

        figure.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        return figure

    @state.change(
        "selected_array",
        "selected_assembly",
        "selected_layer",
        "selected_i",
        "selected_j",
    )
    @ctrl.add("on_vera_out_active_state_index_changed")
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
        ctrl.update_axial_plot(create_line(selected_array, indices))

    with DivLayout(server, template_name="axial_plot") as layout:
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
        ctrl.update_axial_plot = figure.update
