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

    # A cache of core images.
    cached_core_images = {}

    @state.change("selected_time", "selected_array", "selected_layer")
    def update_core_view(selected_time, selected_array, selected_layer, **kwargs):
        selected_layer = int(selected_layer)
        image_data = None

        # Extract from cache if possible
        cache_key = (selected_layer, selected_array, selected_time)
        if cache_key in cached_core_images:
            # Shortcut if we have a cache. We might still need to redraw
            # if the figure size was updated.
            image_data = cached_core_images[cache_key]

        # Extract data from H5 + add to cache
        if image_data is None:
            array = getattr(vera_out_file.active_state, selected_array)
            control_rod_positions = vera_out_file.core.control_rod_positions

            # Load the layer and swap axes for faster indexing
            layer_array = array[:, :, selected_layer].swapaxes(0, 2)

            reduced_core_map = vera_out_file.core.reduced_core_map
            map_shape = reduced_core_map.shape

            # Create the full sized image
            image_shape = (map_shape[0] * array.shape[0], map_shape[1] * array.shape[1])
            image_data = np.empty(image_shape, dtype=array.dtype)

            # Populate it with the arrays
            for i in range(reduced_core_map.shape[0]):
                i_slice = slice(i * array.shape[0], (i + 1) * array.shape[0])
                for j in range(reduced_core_map.shape[1]):
                    j_slice = slice(j * array.shape[1], (j + 1) * array.shape[1])
                    index = reduced_core_map[i, j]
                    if index == 0:
                        # Empty
                        image_data[i_slice, j_slice] = np.nan
                        continue

                    assembly_array = layer_array[index - 1]

                    # Set control rod positions to be nan
                    assembly_array[control_rod_positions] = np.nan

                    image_data[i_slice, j_slice] = assembly_array

            # Only allow one image in the cache
            MAX_ITEMS_IN_CACHE = 1
            while len(cached_core_images) >= MAX_ITEMS_IN_CACHE:
                cached_core_images.pop(next(iter(cached_core_images)))

            cached_core_images[cache_key] = image_data

        # custom widget update
        reduced_core_map = vera_out_file.core.reduced_core_map
        assembly_width = array.shape[0]
        core_width = map_shape[0]
        state.core_assemblies = []
        for j in range(core_width):
            line = []
            state.core_assemblies.append(line)
            for i in range(core_width):
                if reduced_core_map[i, j]:
                    assembly = image_data[
                        slice(i * assembly_width, (i + 1) * assembly_width),
                        slice(j * assembly_width, (j + 1) * assembly_width),
                    ]
                    line.append(np.ravel(assembly).tolist())

    with DivLayout(server, template_name="core_view") as layout:
        layout.root.style = "height: 100%;"
        vera.CoreView(
            value=("core_assemblies", []),
            color_preset="jet",
            color_range=("color_range", [0, 3]),
        )
