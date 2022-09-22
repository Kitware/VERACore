from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify, grid, client, html
from . import (
    assembly_view, axial_plot, axial_view, core_view, empty, time_plot
)

DEFAULT_NB_ROWS = 8


def get_next_y_from_layout(layout):
    next_y = 0
    for item in layout:
        y, h = item.get("y", 0), item.get("h", 1)
        if y + h > next_y:
            next_y = y + h
    return next_y


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller
    state.trame__title = "VERACore"

    # Initialize all visualizations
    state.setdefault("grid_options", [])
    state.setdefault("grid_layout", [])
    assembly_view.initialize(server, vera_out_file)
    axial_plot.initialize(server, vera_out_file)
    axial_view.initialize(server, vera_out_file)
    core_view.initialize(server, vera_out_file)
    time_plot.initialize(server, vera_out_file)
    empty.initialize(server)

    # Reserve the various views
    available_view_ids = [f"{v+1}" for v in range(10)]
    for view_id in available_view_ids:
        state[f"grid_view_{view_id}"] = empty.OPTION

    # Axial view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=0, y=0, w=6, h=12, i=view_id),
    )
    state[f"grid_view_{view_id}"] = axial_view.OPTION

    # Time plot
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=6, y=0, w=6, h=12, i=view_id),
    )
    state[f"grid_view_{view_id}"] = time_plot.OPTION

    # Core view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=0, y=12, w=6, h=12, i=view_id),
    )
    state[f"grid_view_{view_id}"] = core_view.OPTION

    # Axial plot
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=6, y=12, w=6, h=12, i=view_id),
    )
    state[f"grid_view_{view_id}"] = axial_plot.OPTION

    # Assembly view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=0, y=24, w=6, h=12, i=view_id),
    )
    state[f"grid_view_{view_id}"] = assembly_view.OPTION

    @ctrl.set("grid_add_view")
    def add_view():
        next_view_id = available_view_ids.pop()
        next_y = get_next_y_from_layout(state.grid_layout)
        state.grid_layout.append(
            dict(x=0, w=12, h=DEFAULT_NB_ROWS, y=next_y, i=next_view_id)
        )
        state.dirty("grid_layout")

    @ctrl.set("grid_remove_view")
    def remove_view(view_id):
        available_view_ids.append(view_id)
        state.grid_layout = list(
            filter(lambda item: item.get("i") != view_id, state.grid_layout)
        )

    # Setup main layout
    with SinglePageWithDrawerLayout(server) as layout:
        # Toolbar
        layout.title.set_text("VERACore")
        with layout.toolbar as toolbar:
            layout.icon
            toolbar.height = 36
            vuetify.VSpacer()

            vuetify.VSelect(
                v_model=("selected_array", "pin_powers"),
                items=(
                    "available_arrays",
                    [
                        dict(text="Pin Powers", value="pin_powers"),
                        dict(text="Pin Clad Temps", value="pin_cladtemps"),
                        dict(text="Pin Fuel Temps", value="pin_fueltemps"),
                        dict(text="Pin Moderator Density", value="pin_moddens"),
                        dict(text="Pin Moderator Temps", value="pin_modtemps"),
                    ],
                ),
                hide_details=True,
                dense=True,
                style="max-width: 220px",
            )

            with vuetify.VBtn(icon=True, click=ctrl.grid_add_view):
                vuetify.VIcon("mdi-plus")

        with layout.drawer:
            with vuetify.VCard(classes="pt-6"):
                with vuetify.VCardText():
                    data_shape = vera_out_file.core.pin_volumes.shape
                    # The values are the (default, maxes)
                    index_names = {
                        "selected_assembly": (36, data_shape[3]),
                        "selected_layer": (24, data_shape[2]),
                        "selected_i": (7, data_shape[0]),
                        "selected_j": (7, data_shape[1]),
                    }

                    for index_name, (default, maximum) in index_names.items():
                        vuetify.VSlider(
                            v_model=(index_name, default),
                            label=index_name,
                            min=0,
                            max=maximum,
                            thumb_label="always",
                        )

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                with grid.GridLayout(
                    layout=("grid_layout", []),
                    row_height=30,
                    vertical_compact=True,
                    style="width: 100%; height: 100%;",
                ):
                    with grid.GridItem(
                        v_for="item in grid_layout",
                        key="item.i",
                        v_bind="item",
                        style="touch-action: none;",
                        drag_ignore_from=".drag_ignore",
                    ):
                        with vuetify.VCard(style="height: 100%;"):
                            with vuetify.VCardTitle(classes="py-1 px-1"):
                                with vuetify.VMenu(offset_y=True):
                                    with vuetify.Template(
                                        v_slot_activator="{ on, attrs }"
                                    ):
                                        with vuetify.VBtn(
                                            icon=True,
                                            small=True,
                                            v_bind="attrs",
                                            v_on="on",
                                        ):
                                            vuetify.VIcon(
                                                v_text="get(`grid_view_${item.i}`).icon"
                                            )
                                        html.Div(
                                            "{{ get(`grid_view_${item.i}`).label }}",
                                            classes="ml-1 text-subtitle-2",
                                        )
                                    with vuetify.VList(dense=True):
                                        with vuetify.VListItem(
                                            v_for="(option, index) in grid_options",
                                            key="index",
                                            click="set(`grid_view_${item.i}`, option)",
                                        ):
                                            with vuetify.VListItemIcon():
                                                vuetify.VIcon(v_text="option.icon")
                                            vuetify.VListItemTitle("{{ option.label }}")
                                vuetify.VSpacer()
                                with vuetify.VBtn(
                                    icon=True,
                                    x_small=True,
                                    click=(ctrl.grid_remove_view, "[item.i]"),
                                ):
                                    vuetify.VIcon(
                                        "mdi-delete-forever-outline", small=True
                                    )
                            vuetify.VDivider()

                            style = "; ".join(
                                [
                                    "position: relative",
                                    "height: calc(100% - 37px)",
                                    "overflow: auto",
                                ]
                            )
                            with vuetify.VCardText(style=style, classes="drag_ignore"):
                                # Add template for value of get(`grid_view_${item.i}`)
                                client.ServerTemplate(
                                    name=("get(`grid_view_${item.i}`).name",)
                                )

        # Footer
        # layout.footer.hide()
