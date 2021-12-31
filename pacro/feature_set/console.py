import copy

from textual.app import App
from textual import events
from textual.widgets import *
import rich
import rich.repr
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from .config import *
from textual.widget import Widget
from textual.view import View
from textual.layouts.vertical import VerticalLayout
from textual.reactive import Reactive


class CheckboxItem(Widget):
    enabled = Reactive(False)
    selected = Reactive(False)

    def __init__(self, parent: Widget, *, key: str, explain: str, enabled: bool, selected: bool = False) -> None:
        super().__init__()
        self._parent = parent
        self.key = key
        self.explain = explain
        self.enabled = enabled
        self.selected = selected

    def __rich_repr__(self) -> rich.repr.Result:
        yield "enabled", self.enabled
        yield "label", self.key

    def render(self) -> Table:
        grid = Table.grid(padding=1)
        grid.add_column()
        grid.add_row(
            "\\[x]" if self.enabled else "[ ]",
            self.key,
            self.explain,
            style=Style(reverse=self.selected),
        )

        return grid

    async def on_click(self, event: events.Click) -> None:
        event.prevent_default().stop()
        await self.emit(ButtonPressed(self))


class FeatureList(View, layout=VerticalLayout, can_focus=True):
    name = 'feature list'
    selection = Reactive(None)

    def __init__(self, feature_set: CompiledFeatureSet) -> None:
        super().__init__()
        self.feature_set = feature_set
        self.selection = None

        self.features = []
        for i, feature in enumerate(self.feature_set.features):
            name = feature.name
            if not feature.take_value:
                rely_on = self.feature_set.get_dependencies(name)
                if rely_on:
                    rely_on = " rely on \\[" + ', '.join(rely_on) + ']'
                else:
                    rely_on = ""
                wg = CheckboxItem(
                    self,
                    key=feature.name,
                    explain=feature.description + rely_on,
                    enabled=self.feature_set.values.get(name),
                    selected=False,
                )
                self.features.append(wg)
                self.layout.add(wg)

    @property
    def features_num(self):
        return len(self.features)

    def handle_button_pressed(self, message: ButtonPressed) -> None:
        self.feature_set.set(message.sender.key, not message.sender.enabled)
        for feature in self.features:
            feature.enabled = self.feature_set.values[feature.key]

    def on_key(self, event: events.Key):
        if self.selection is None:
            if event.key == events.Keys.Up:
                self.selection = self.features_num - 1
            elif event.key == events.Keys.Down:
                self.selection = 0
            if event.key == events.Keys.Up or event.key == events.Keys.Down:
                self.features[self.selection].selected = True

        elif event.key == events.Keys.Up or event.key == events.Keys.Down:
            self.features[self.selection].selected = False
            if event.key == events.Keys.Up:
                self.selection = (self.selection + self.features_num - 1) % self.features_num

            if event.key == events.Keys.Down:
                self.selection = (self.selection + 1) % self.features_num
            self.features[self.selection].selected = True
        elif event.key == events.Keys.Enter or event.key == " ":
            self.handle_button_pressed(ButtonPressed(self.features[self.selection]))


class FeatureSelector(App):
    def __init__(self, feature_set: CompiledFeatureSet, **kwargs):
        super().__init__(**kwargs)
        self.feature_set = feature_set

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("q", "quit", "Quit & Save")
        await self.bind("enter/space", "enter", "Confirm")
        await self.bind("up/down", "arrow", "Cursor Up/Down")

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""

        fl = FeatureList(self.feature_set)

        # Header / footer / dock
        await self.view.dock(Footer(), edge="bottom")

        # Dock the body in the remaining space
        await self.view.dock(fl, edge="right")


def display(feature_set: CompiledFeatureSet):
    FeatureSelector.run(title="Select features", feature_set=feature_set)
