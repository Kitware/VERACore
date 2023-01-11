import numpy as np

from trame.ui.vuetify import SinglePageLayout
from trame.widgets import client, grid, html, vuetify
from vera_core.widgets import vera
from . import (
    assembly_view,
    axial_plot,
    core_view,
    empty,
    table_view,
    time_plot,
    x_axial_view,
    y_axial_view,
    volume_view,
    assets,
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

    state.setdefault("grid_item_dirty_key", 0)

    # FIXME: For our example, fix this to match VeraView.
    # Come up with a way to autogenerate it.
    state.color_range = (0.0273, 1.95)
    state.selected_layer = 24
    state.selected_assembly = 36
    state.selected_time = 0
    # FIXME ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    @state.change("selected_time")
    def selected_time_changed(selected_time, **kwargs):
        selected_time = int(selected_time)
        vera_out_file.active_state_index = selected_time

        ctrl.on_vera_out_active_state_index_changed(
            selected_time=selected_time, **kwargs
        )

    @state.change("selected_array")
    def selected_array_changed(selected_array, **kwargs):
        array = vera_out_file.array(selected_array)
        state.color_range = (np.nanmin(array), np.nanmax(array))

    # Keep selected_assembly and selected_assembly_ij in sync
    @state.change("selected_assembly_ij")
    def selected_assembly_ij_changed(selected_assembly_ij, **kwargs):
        i, j = selected_assembly_ij["i"], selected_assembly_ij["j"]
        state.selected_assembly = vera_out_file.core.reduced_core_map_assembly(i, j)

    @state.change("selected_assembly")
    def selected_assembly_changed(selected_assembly, **kwargs):
        i, j = vera_out_file.core.reduced_core_map_ij(selected_assembly)
        state.selected_assembly_ij = dict(i=i, j=j)

    # Go ahead and make sure they are in sync
    selected_assembly_changed(state.selected_assembly)

    # Initialize all visualizations
    state.setdefault("grid_options", [])
    state.setdefault("grid_layout", [])
    assembly_view.initialize(server, vera_out_file)
    axial_plot.initialize(server, vera_out_file)
    x_axial_view.initialize(server, vera_out_file)
    y_axial_view.initialize(server, vera_out_file)
    core_view.initialize(server, vera_out_file)
    table_view.initialize(server, vera_out_file)
    time_plot.initialize(server, vera_out_file)
    volume_view.initialize(server, vera_out_file)
    empty.initialize(server)

    # Reserve the various views
    available_view_ids = [f"{v+1}" for v in range(10)]
    for view_id in available_view_ids:
        state[f"grid_view_{view_id}"] = empty.OPTION

    # X Axial view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=0, y=0, w=3, h=17, i=view_id),
    )
    state[f"grid_view_{view_id}"] = x_axial_view.OPTION

    # Y Axial view
    # view_id = available_view_ids.pop(0)
    # state.grid_layout.append(
    #     dict(x=3, y=0, w=3, h=17, i=view_id),
    # )
    # state[f"grid_view_{view_id}"] = y_axial_view.OPTION

    # Core view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=6, y=0, w=3, h=9, i=view_id),
    )
    state[f"grid_view_{view_id}"] = core_view.OPTION

    # Assembly view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=9, y=0, w=3, h=9, i=view_id),
    )
    state[f"grid_view_{view_id}"] = assembly_view.OPTION

    # Axial plot
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=6, y=9, w=3, h=8, i=view_id),
    )
    state[f"grid_view_{view_id}"] = axial_plot.OPTION

    # Time plot
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=9, y=9, w=3, h=8, i=view_id),
    )
    state[f"grid_view_{view_id}"] = time_plot.OPTION

    # Volume view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=3, y=0, w=3, h=17, i=view_id),
    )
    state[f"grid_view_{view_id}"] = volume_view.OPTION

    # Table view
    view_id = available_view_ids.pop(0)
    state.grid_layout.append(
        dict(x=0, y=17, w=6, h=10, i=view_id),
    )
    state[f"grid_view_{view_id}"] = table_view.OPTION

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
    with SinglePageLayout(server) as layout:
        layout.root.classes = ("{ busy: trame__busy }",)

        # Toolbar
        with layout.toolbar as toolbar:
            toolbar.clear()

            toolbar.height = 36

            html.Img(src=assets.LOGO, height=25)
            vuetify.VSpacer()

            vera.ColorMapEditor(
                v_model="color_range",
                color_preset="jet",
            )

            vuetify.VSpacer()

            with html.Div(
                style="width: 25px",
                classes="mr-2",
            ):
                vuetify.VProgressCircular(
                    indeterminate=True,
                    v_show=("trame__busy",),
                    style="background-color: lightgray; border-radius: 50%",
                    background_opacity=1,
                    bg_color="#01549b",
                    color="#04a94d",
                    size=16,
                    width=3,
                )

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
                        dict(text="Pin Volumes", value="pin_volumes"),
                    ],
                ),
                hide_details=True,
                dense=True,
                style="max-width: 220px",
            )

            with vuetify.VBtn(icon=True, click=ctrl.grid_add_view):
                vuetify.VIcon("mdi-plus")

        # Main content
        with layout.content:
            layout.content.style = "overflow: auto; margin: 36px 0px 35px; padding: 0;"
            with vuetify.VContainer(
                fluid=True,
                classes="pa-0 fill-height",
                style="user-select: none;",
            ):
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
                        with vuetify.VCard(
                            style="height: 100%;",
                            key="grid_item_dirty_key",
                        ):
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
                                            click="""
                                                set(`grid_view_${item.i}`, option);
                                                grid_item_dirty_key++;
                                            """,
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
        with layout.footer as footer:
            footer.clear()

            footer.height = 35
            with vuetify.VBtn(
                icon=True,
                small=True,
                disabled=("selected_time == 0",),
                click="selected_time--",
            ):
                vuetify.VIcon("mdi-minus")
            html.Div(
                "State {{ selected_time }}",
                classes="text-center",
                style="width: 100px;",
            )
            with vuetify.VBtn(
                icon=True,
                small=True,
                disabled=(f"selected_time == {len(vera_out_file.states) - 1}",),
                click="selected_time++",
            ):
                vuetify.VIcon("mdi-plus")
            vuetify.VDivider(vertical=True, classes="mx-2")
            vuetify.VSlider(
                v_model=("selected_time",),
                min=0,
                max=len(vera_out_file.states) - 1,
                dense=True,
                hide_details=True,
                ticks="always",
                tick_size="4",
                height=35,
                # style="position: relative; top: -10px;",
                # tick_labels=(f"[{','.join([str(v) for v in range(len(vera_out_file.states))])}]", ),
            )
