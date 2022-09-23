import numpy as np

from trame.ui.html import DivLayout
from vera_core.widgets import vera

OPTION = {
    "name": "core_view",
    "label": "Core View",
    "icon": "mdi-chart-donut-variant",
}


def initialize(server, vera_out_file):
    state = server.state

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    state.selected_assembly_ij = {"i": 4, "j": 4}

    @state.change("selected_assembly_ij")
    def selected_assembly_ij_changed(selected_assembly_ij, **kwargs):
        i, j = selected_assembly_ij["i"], selected_assembly_ij["j"]
        reduced_core_map = vera_out_file.core.reduced_core_map
        state.selected_assembly = int(reduced_core_map[j, i] - 1)

    @state.change("selected_time", "selected_array", "selected_layer")
    def update_core_view(selected_array, selected_layer, **kwargs):
        selected_layer = int(selected_layer)

        array = getattr(vera_out_file.active_state, selected_array)

        # Load the layer and swap axes for faster indexing
        layer_array = array[:, :, selected_layer].swapaxes(0, 2)
        layer_array = layer_array.swapaxes(1, 2)

        control_rod_positions = vera_out_file.core.control_rod_positions
        reduced_core_map = vera_out_file.core.reduced_core_map
        core_width = reduced_core_map.shape[0]

        # custom widget update
        state.core_assemblies = []
        for i in range(core_width):
            line = []
            state.core_assemblies.append(line)
            for j in range(core_width):
                index = reduced_core_map[i, j] - 1
                if index == -1:
                    continue

                assembly_array = layer_array[index]

                # Set control rod positions to be nan
                assembly_array[control_rod_positions] = np.nan

                line.append(np.ravel(assembly_array).tolist())

    with DivLayout(server, template_name="core_view") as layout:
        layout.root.style = "height: 100%;"
        vera.CoreView(
            value=("core_assemblies", []),
            selected_i=("selected_assembly_ij.i",),
            selected_j=("selected_assembly_ij.j",),
            color_preset="jet",
            color_range=("color_range", [0, 3]),
            click="selected_assembly_ij = $event",
        )
