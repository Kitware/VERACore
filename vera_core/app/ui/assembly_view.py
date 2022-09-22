import matplotlib.pyplot as plt
import numpy as np

from trame.ui.html import DivLayout

from trame.widgets import matplotlib, trame

OPTION = {
    "name": "assembly_view",
    "label": "Assembly View",
    "icon": "mdi-chart-donut-variant",
}

plt.set_cmap("jet")


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller

    # Create the figure and axes we will use
    fig, ax = plt.subplots()
    colorbar = None

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    def figure_size():
        if state.assembly_view_size is None:
            return {}

        dpi = 96
        rect = state.assembly_view_size.get("size")
        w_inch = rect.get("width") / dpi * 0.8  # Reduce width to better use space
        h_inch = rect.get("height") / dpi

        return {
            "figsize": (w_inch, h_inch),
            "dpi": dpi,
        }

    def create_image(img):
        figsize_dict = figure_size()
        if "figsize" in figsize_dict:
            width, height = figsize_dict["figsize"]
            fig.set_figwidth(width)
            fig.set_figheight(height)

        if "dpi" in figsize_dict:
            dpi = figsize_dict["dpi"]
            fig.set_dpi(dpi)

        # FIXME: why are we still getting interpolation in our app?
        axes_image = ax.imshow(img, interpolation="nearest")

        # Make the color ranges match
        clim = state.color_range
        if clim is not None:
            axes_image.set_clim(clim)

        nonlocal colorbar
        if colorbar:
            colorbar.remove()

        colorbar = fig.colorbar(axes_image)
        return fig

    # A cache of assembly images.
    cached_assembly_images = {}

    @state.change(
        "assembly_view_size",
        "selected_time",
        "selected_array",
        "selected_assembly",
        "selected_layer",
        "color_range",
    )
    def update_assembly_view(
        selected_time, selected_array, selected_assembly, selected_layer,
        **kwargs
    ):
        selected_assembly = int(selected_assembly)
        selected_layer = int(selected_layer)

        cache_key = (selected_time, selected_array, selected_assembly,
                     selected_layer)
        if cache_key in cached_assembly_images:
            # Shortcut if we have a cache. We might still need to redraw
            # if the figure size was updated.
            image_data = cached_assembly_images[cache_key]
            ctrl.update_assembly_figure(create_image(image_data))
            return

        array = getattr(vera_out_file.active_state, selected_array)

        image = array[:, :, selected_layer, selected_assembly]

        control_rod_positions = vera_out_file.core.control_rod_positions

        # Make control rod positions equal to nan
        image[control_rod_positions] = np.nan

        # Only allow one image in the cache
        MAX_ITEMS_IN_CACHE = 1
        while len(cached_assembly_images) >= MAX_ITEMS_IN_CACHE:
            cached_assembly_images.pop(next(iter(cached_assembly_images)))

        cached_assembly_images[cache_key] = image

        ctrl.update_assembly_figure(create_image(image))

    with DivLayout(server, template_name="assembly_view") as layout:
        layout.root.style = "height: 100%;"
        with trame.SizeObserver("assembly_view_size"):
            html_figure = matplotlib.Figure()
            ctrl.update_assembly_figure = html_figure.update
