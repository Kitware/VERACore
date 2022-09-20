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
        fig, ax = plt.subplots(**figure_size())
        axes_image = ax.imshow(img)
        fig.colorbar(axes_image)
        return fig

    # A cache of axial images.
    cached_axial_images = {}

    @state.change("figure_size", "selected_array", "selected_assembly",
                  "selected_j")
    def update_axial_view(selected_array, selected_assembly, selected_j,
                          **kwargs):
        selected_assembly = int(selected_assembly)
        selected_j = int(selected_j)

        row_assembly_indices = vera_out_file.core.row_assembly_indices(
            selected_assembly)

        cache_key = (tuple(row_assembly_indices), selected_array)
        if cache_key in cached_axial_images:
            # Shortcut if we have a cache. We might still need to redraw
            # if the figure size was updated.
            image_data = cached_axial_images[cache_key]
            ctrl.update_figure(create_image(image_data))
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

        ctrl.update_figure(create_image(image_data))

    with DivLayout(server, template_name="axial_view") as layout:
        # FIXME: why can't we use trame.SizeObserver() here?
        # with trame.SizeObserver("figure_size"):
        html_figure = matplotlib.Figure(style="position: absolute")
        ctrl.update_figure = html_figure.update
