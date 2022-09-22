import matplotlib.pyplot as plt
import numpy as np

from trame.ui.html import DivLayout

from trame.widgets import matplotlib, trame

OPTION = {
    "name": "axial_view",
    "label": "Axial View",
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
        if state.axial_view_size is None:
            return {}

        dpi = 96
        rect = state.axial_view_size.get("size")
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
            fig.set_width(width)
            fig.set_height(height)

        if "dpi" in figsize_dict:
            dpi = figsize_dict["dpi"]
            fig.set_depi(dpi)

        axes_image = ax.imshow(img)

        # The axial image determines the color range
        state.color_range = axes_image.get_clim()

        nonlocal colorbar
        if colorbar:
            colorbar.remove()

        colorbar = fig.colorbar(axes_image)
        return fig

    # A cache of axial images.
    cached_axial_images = {}

    @state.change(
        "figure_size",
        "selected_array",
        "selected_assembly",
        "selected_j",
        "axial_view_size",
    )
    def update_axial_view(selected_array, selected_assembly, selected_j, **kwargs):
        selected_assembly = int(selected_assembly)
        selected_j = int(selected_j)

        row_assembly_indices = vera_out_file.core.row_assembly_indices(
            selected_assembly
        )

        cache_key = (tuple(row_assembly_indices), selected_array)
        if cache_key in cached_axial_images:
            # Shortcut if we have a cache. We might still need to redraw
            # if the figure size was updated.
            image_data = cached_axial_images[cache_key]
            ctrl.update_axial_figure(create_image(image_data))
            return

        array = getattr(vera_out_file.active_state, selected_array)
        # Numpy will tack the indexing subspace on to the beginning
        image_data = array[selected_j, :, :, row_assembly_indices]
        image_data = np.vstack(image_data).T

        # For the heights, we will use vera_out_file.core.axial_mesh_pixels
        # and maybe np.repeat() to repeat the values to make the pixels the
        # right height (which will reflect their actual assembly height).
        axial_pixels = vera_out_file.core.axial_mesh_pixels
        image_data = np.repeat(image_data, axial_pixels, axis=0)

        # Have to reverse the y-axis since ax.invert_yaxis() doesn't work here
        image_data = image_data[::-1, :]

        # Only allow one image in the cache
        MAX_ITEMS_IN_CACHE = 1
        while len(cached_axial_images) >= MAX_ITEMS_IN_CACHE:
            cached_axial_images.pop(next(iter(cached_axial_images)))

        cached_axial_images[cache_key] = image_data

        ctrl.update_axial_figure(create_image(image_data))

    with DivLayout(server, template_name="axial_view") as layout:
        layout.root.style = "height: 100%;"
        with trame.SizeObserver("axial_view_size"):
            html_figure = matplotlib.Figure()
            ctrl.update_axial_figure = html_figure.update
