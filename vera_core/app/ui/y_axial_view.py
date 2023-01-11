import numpy as np

from trame.ui.html import DivLayout
from vera_core.widgets import vera

OPTION = {
    "name": "y_axial_view",
    "label": "Y Axial View",
    "icon": "mdi-border-vertical",
}


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    def axial_cell_selected(layer, assembly_j):
        assembly_i = state.selected_assembly_ij["i"]
        state.selected_assembly = vera_out_file.core.reduced_core_map_assembly(
            assembly_i, assembly_j
        )
        state.selected_layer = layer

    @state.change(
        "selected_array",
        "selected_assembly",
        "selected_i",
    )
    @ctrl.add("on_vera_out_active_state_index_changed")
    def update_axial_view(selected_array, selected_assembly, selected_i, **kwargs):
        selected_assembly = int(selected_assembly)
        selected_i = int(selected_i)
        col_assembly_indices = vera_out_file.core.col_assembly_indices(
            selected_assembly
        )
        array = vera_out_file.array(selected_array)
        assembly_size = array.shape[0]

        # Numpy will tack the indexing subspace on to the beginning
        image_data = array[:, selected_i, :, col_assembly_indices]
        image_data = np.vstack(image_data).T

        # Have to reverse the y-axis since ax.invert_yaxis() doesn't work here
        image_data = image_data[::-1, :]

        # Extract cell sizes
        nb_lines = image_data.shape[0]
        nb_cols = int(image_data.shape[1] / assembly_size)
        state.y_axial_core_size_y = vera_out_file.core.axial_mesh_pixels.tolist()
        state.y_axial_core_size_x = [assembly_size for i in range(nb_cols)]
        state.y_axial_core_label_y = [
            i + 1 for i in range(len(state.y_axial_core_size_y))
        ]
        state.y_axial_core_label_y.reverse()

        # Update UI
        state.y_axial_core = []
        for j in range(nb_lines):
            line = []
            state.y_axial_core.append(line)
            for i in range(nb_cols):
                assembly = image_data[
                    j, slice(i * assembly_size, (i + 1) * assembly_size)
                ]
                line.append(np.ravel(assembly).tolist())

    # Convert these to 1-based indexing
    start_x = vera_out_file.core.reduced_core_map_start_index + 1
    stop_x = len(vera_out_file.core.core_map) + 1

    with DivLayout(server, template_name="y_axial_view") as layout:
        layout.root.style = "height: 100%;"
        vera.AxialView(
            value=("y_axial_core", []),
            color_preset="jet",
            color_range=("color_range", [0, 3]),
            x_sizes=("y_axial_core_size_x", []),
            y_sizes=("y_axial_core_size_y", []),
            x_labels=("y_axial_core_label_x", list(range(start_x, stop_x))),
            y_labels=("y_axial_core_label_y", []),
            selected_i=("selected_assembly_ij.j",),
            selected_j=("y_axial_core_label_y.length - selected_layer - 1",),
            click=(
                axial_cell_selected,
                "[y_axial_core_label_y.length - $event.j - 1, $event.i]",
            ),
            x_scale=("3",),
            y_scale=("3",),
            busy=("trame__busy",),
        )
