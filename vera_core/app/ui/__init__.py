from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, grid, client, trame
from . import power_over_time, top_quadrant, empty


def get_next_y_from_layout(layout):
    next_y = 0
    for item in layout:
        y, h = item.get("y", 0), item.get("h", 1)
        if y + h > next_y:
            next_y = y + h
    return next_y


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "VERACore"

    # Initialize all visualizations
    state.setdefault("grid_options", [])
    power_over_time.initialize(server)
    top_quadrant.initialize(server)
    empty.initialize(server)

    # Reserve the various views
    available_view_ids = [f"{v+1}" for v in range(10)]
    for view_id in available_view_ids:
        state[f"grid_view_{view_id}"] = "empty"

    @ctrl.set("grid_add_view")
    def add_view():
        next_view_id = available_view_ids.pop()
        next_y = get_next_y_from_layout(state.grid_layout)
        state.grid_layout.append(dict(x=0, w=12, h=1, y=next_y, i=next_view_id))
        state.dirty("grid_layout")

    @ctrl.set("grid_remove_view")
    def remove_view(view_id):
        print("remove_view", view_id)
        available_view_ids.append(view_id)
        state.grid_layout = filter(
            lambda item: item.get("i") != view_id, state.grid_layout
        )

    state.new_grid_layout = []

    @state.change("new_grid_layout")
    def on_layout_change(new_grid_layout, **kwargs):
        print("in", new_grid_layout)
        result = []
        for item in new_grid_layout:
            new_item = dict(**item)
            new_item.pop("moved")
            result.append(new_item)

        print(result)
        state.grid_layout = result

    # @state.change("content_size")
    # def on_size_change(content_size, **kwargs):
    #     print(content_size)

    # Setup main layout
    with SinglePageLayout(server) as layout:
        # Toolbar
        layout.title.set_text("VERACore")
        with layout.toolbar as toolbar:
            toolbar.dense = True
            vuetify.VSpacer()
            with vuetify.VBtn(icon=True, click=ctrl.grid_add_view):
                vuetify.VIcon("mdi-plus")

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                with trame.SizeObserver("content_size"):
                    with grid.GridLayout(
                        layout=("grid_layout", []),
                        layout_updated="new_grid_layout = $event",
                        row_height=100,
                        max_rows=3,
                        # max_rows=("Math.floor(content_size?.size?.height / 200) || 10",),
                        classes="fill-height",
                        style="width: 100%; position: relative;",
                    ):
                        with grid.GridItem(
                            v_for="item in grid_layout",
                            key="item.i",
                            v_bind="item",
                        ):
                            with vuetify.VCard(style="height: 100%;"):
                                with vuetify.VCardTitle(classes="py-0"):
                                    vuetify.VSelect(
                                        value=("get(`grid_view_${item.i}`)",),
                                        change="set(`grid_view_${item.i}`, $event)",
                                        items=("grid_options", []),
                                        dense=True,
                                        hide_details=True,
                                    )
                                    vuetify.VSpacer()
                                    with vuetify.VBtn(
                                        icon=True,
                                        click=(ctrl.grid_remove_view, "[item.i]"),
                                    ):
                                        vuetify.VIcon("mdi-delete-forever-outline")
                                vuetify.VDivider()
                                with vuetify.VCardText():
                                    # Add template for value of get(`grid_view_${item.i}`)
                                    client.ServerTemplate(
                                        name=("get(`grid_view_${item.i}`)",)
                                    )

        # Footer
        # layout.footer.hide()
