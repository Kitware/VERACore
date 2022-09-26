from trame_client.widgets.core import AbstractElement
from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


class AssemblyView(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "vera-assembly-view",
            **kwargs,
        )
        self._attr_names += [
            "value",
            ("selected_i", "selectedI"),
            ("selected_j", "selectedJ"),
            ("color_preset", "colorPreset"),
            ("color_range", "colorRange"),
            ("active_style", ":activeStyle"),
        ]
        self._event_names += [
            "click",
        ]


class CoreView(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "vera-core-view",
            **kwargs,
        )
        self._attr_names += [
            "value",
            ("selected_i", "selectedI"),
            ("selected_j", "selectedJ"),
            ("color_preset", "colorPreset"),
            ("color_range", "colorRange"),
            ("active_style", ":activeStyle"),
            ("x_labels", "xLabels"),
            ("y_labels", "yLabels"),
            "scaling",
        ]
        self._event_names += [
            "click",
        ]


class AxialView(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "vera-axial-view",
            **kwargs,
        )
        self._attr_names += [
            "value",
            ("selected_i", "selectedI"),
            ("selected_j", "selectedJ"),
            ("color_preset", "colorPreset"),
            ("color_range", "colorRange"),
            ("active_style", ":activeStyle"),
            ("x_labels", "xLabels"),
            ("y_labels", "yLabels"),
            ("x_scale", "xScale"),
            ("y_scale", "yScale"),
            ("x_sizes", "xSizes"),
            ("y_sizes", "ySizes"),
        ]
        self._event_names += [
            "click",
        ]


class ColorMapEditor(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "vera-color-map-editor",
            **kwargs,
        )
        self._attr_names += [
            "value",
            ("color_preset", "colorPreset"),
        ]
        self._event_names += [
            "input",
        ]
