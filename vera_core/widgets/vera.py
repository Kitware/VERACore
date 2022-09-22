from trame_client.widgets.core import AbstractElement
from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


# Expose your vue component(s)
class TopQuadrant(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "vera-top-quadrant",
            **kwargs,
        )
        self._attr_names += [
            "size",
            ("x_labels", "xLabels"),
            ("y_labels", "yLabels"),
            "value",
            ("quadrant_values", "quadrantValues"),
            ("color_preset", "colorPreset"),
            ("color_range", "colorRange"),
        ]
        self._event_names += [
            "click",
        ]


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
