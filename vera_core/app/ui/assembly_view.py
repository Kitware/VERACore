import matplotlib.pyplot as plt
import numpy as np

from trame.ui.html import DivLayout

from trame.widgets import matplotlib

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
        if state.figure_size is None:
            return {}

        dpi = state.figure_size.get("dpi")
        rect = state.figure_size.get("size")
        w_inch = rect.get("width") / dpi
        h_inch = rect.get("height") / dpi

        # FIXME: the height isn't working. It is always 0.

        return {
            "figsize": (w_inch, h_inch),
            "dpi": dpi,
        }

    def create_image(img):
        figsize_dict = figure_size()
        if "figsize" in figsize_dict:
            width, height = figsize_dict["figsize"]
            fig.set_width(width)
            fig.set_height(height)

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
        "figure_size",
        "selected_array",
        "selected_assembly",
        "selected_layer",
        "color_range",
    )
    def update_assembly_view(
        selected_array, selected_assembly, selected_layer, **kwargs
    ):
        selected_assembly = int(selected_assembly)
        selected_layer = int(selected_layer)

        cache_key = (selected_array, selected_assembly, selected_layer)
        if cache_key in cached_assembly_images:
            # Shortcut if we have a cache. We might still need to redraw
            # if the figure size was updated.
            image_data = cached_assembly_images[cache_key]
            ctrl.update_figure(create_image(image_data))
            return

        array = getattr(vera_out_file.active_state, selected_array)

        image = array[:, :, selected_layer, selected_assembly]

        if selected_array == "pin_powers":
            # Make anywhere that is zero be nan
            image[np.where(image == 0)] = np.nan

        # Only allow one image in the cache
        MAX_ITEMS_IN_CACHE = 1
        while len(cached_assembly_images) >= MAX_ITEMS_IN_CACHE:
            cached_assembly_images.pop(next(iter(cached_assembly_images)))

        cached_assembly_images[cache_key] = image

        ctrl.update_figure(create_image(image))

    with DivLayout(server, template_name="assembly_view"):
        # FIXME: why can't we use trame.SizeObserver() here?
        # with trame.SizeObserver("figure_size"):
        html_figure = matplotlib.Figure(style="position: absolute")
        ctrl.update_figure = html_figure.update
