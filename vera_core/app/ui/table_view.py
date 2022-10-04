from trame.ui.html import DivLayout
from trame.widgets import vuetify


OPTION = {
    "name": "table_view",
    "label": "Table View",
    "icon": "mdi-table",
}


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    @state.change(
        "selected_array",
        "selected_assembly",
        "selected_layer",
        "selected_i",
        "selected_j",
    )
    @ctrl.add("on_vera_out_active_state_index_changed")
    def update_table(
        selected_array,
        selected_assembly,
        selected_layer,
        selected_i,
        selected_j,
        **kwargs,
    ):
        indices = (selected_j, selected_i, selected_layer, selected_assembly)
        indices = tuple(map(int, indices))

        array = vera_out_file.array(selected_array)
        value = array[indices]

        data_dict = {
            selected_array: value,
            "crit_boron": vera_out_file.active_state.crit_boron[0],
            "exposure": vera_out_file.active_state.exposure[0],
            "keff": vera_out_file.active_state.keff[0],
        }

        # Round floats so we don't display too many sig figs.
        # 7 sig figs matches veraview.
        sig_figs = 7
        data_dict = {
            k: float(f"{v:0.{sig_figs}g}")
            for k, v in data_dict.items()
            if isinstance(v, float)
        }

        # Create column labels
        axial_value = vera_out_file.core.axial_mesh_means[selected_layer]
        assembly_label = vera_out_file.core.reduced_core_map_label(selected_assembly)
        columns = [
            "Dataset",
            f"Assembly {assembly_label}; Axial {axial_value:0.6g} cm; Pin ({selected_i + 1}, {selected_j + 1})",
        ]

        # Convert into VDataTable format
        headers = [{"text": x, "value": x} for x in columns]

        data = list(data_dict.items())
        rows = [dict(zip(columns, entry)) for entry in data]

        state.table_view_headers = headers
        state.table_view_rows = rows

    table_options = {
        "headers": ("table_view_headers", []),
        "items": ("table_view_rows", []),
        "classes": "mt-n2",
        "disable_sort": True,
        "dense": True,
        "disable_pagination": True,
        # Even though the pagination is disabled, this is necessary to hide it
        "hide_default_footer": True,
    }

    with DivLayout(server, template_name="table_view") as layout:
        layout.root.style = "height: 100%; width: 100%;"
        vuetify.VDataTable(**table_options)
