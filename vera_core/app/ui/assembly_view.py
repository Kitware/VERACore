import numpy as np

from trame.ui.html import DivLayout
from vera_core.widgets import vera

OPTION = {
    "name": "assembly_view",
    "label": "Assembly View",
    "icon": "mdi-dots-grid",
}


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    # A cache of assembly images.
    cached_assembly_images = {}

    @state.change(
        "assembly_view_size",
        "selected_array",
        "selected_assembly",
        "selected_layer",
        "color_range",
    )
    @ctrl.add("on_vera_out_active_state_index_changed")
    def update_assembly_view(
        selected_time, selected_array, selected_assembly, selected_layer, **kwargs
    ):
        selected_assembly = int(selected_assembly)
        selected_layer = int(selected_layer)
        image_data = None

        # Extract from cache if possible
        cache_key = (selected_time, selected_array, selected_assembly, selected_layer)
        if cache_key in cached_assembly_images:
            # Shortcut if we have a cache. We might still need to redraw
            # if the figure size was updated.
            image_data = cached_assembly_images[cache_key]

        # Extract data from H5 + add to cache
        if image_data is None:
            array = vera_out_file.array(selected_array)
            image_data = array[:, :, selected_layer, selected_assembly]
            control_rod_positions = vera_out_file.core.control_rod_positions

            # Make control rod positions equal to nan
            image_data[control_rod_positions] = np.nan

            # Only allow one image in the cache
            MAX_ITEMS_IN_CACHE = 1
            while len(cached_assembly_images) >= MAX_ITEMS_IN_CACHE:
                cached_assembly_images.pop(next(iter(cached_assembly_images)))

            cached_assembly_images[cache_key] = image_data

        # Update the client
        state.assembly_array = np.ravel(image_data).tolist()

    # UI content
    with DivLayout(server, template_name="assembly_view") as layout:
        layout.root.style = "height: 100%;"
        vera.AssemblyView(
            value=("assembly_array", []),
            selected_i=("selected_i", 7),
            selected_j=("selected_j", 7),
            color_preset="jet",
            color_range=("color_range", [0, 3]),
            click="setAll({ selected_i: $event.i, selected_j: $event.j})",
            busy=("trame__busy",),
        )
