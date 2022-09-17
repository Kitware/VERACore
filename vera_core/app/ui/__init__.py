from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, grid, client, html
from . import power_over_time, top_quadrant, empty

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
    power_over_time.initialize(server, vera_out_file)
    top_quadrant.initialize(server, vera_out_file)
    empty.initialize(server)

    # Reserve the various views
    available_view_ids = [f"{v+1}" for v in range(10)]
    for view_id in available_view_ids:
        state[f"grid_view_{view_id}"] = empty.OPTION

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
        # Toolbar
        layout.title.set_text("VERACore")
        with layout.toolbar as toolbar:
            layout.icon
            toolbar.height = 36
            vuetify.VSpacer()

            index_names = [
                "selected_assembly",
                "selected_layer",
                "selected_i",
                "selected_j",
            ]

            for index_name in index_names:
                vuetify.VTextField(
                    v_model=(index_name, 0),
                    label=index_name,
                    hide_details=True,
                    dense=True,
                    type="number",
                    # FIXME: Put in min and max. max=
                    style="max-width: 100px;",
                    classes="mx-1",
                )

            with vuetify.VBtn(icon=True, click=ctrl.grid_add_view):
                vuetify.VIcon("mdi-plus")

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

                            style = "; ".join([
                                "position: relative",
                                "height: calc(100% - 37px)",
                                "overflow: auto",
                            ])
                            with vuetify.VCardText(style=style,
                                                   classes="drag_ignore"):
                                # Add template for value of get(`grid_view_${item.i}`)
                                client.ServerTemplate(
                                    name=("get(`grid_view_${item.i}`).name",)
                                )

        # Footer
        # layout.footer.hide()
