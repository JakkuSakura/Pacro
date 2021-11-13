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

    def __init__(self, parent: Widget, *, label: str, enabled: bool, selected: bool = False, index: int = -1) -> None:
        super().__init__()
        self._parent = parent
        self.label = label
        self.enabled = enabled
        self.selected = selected
        self.index = index

    def __rich_repr__(self) -> rich.repr.Result:
        yield "enabled", self.enabled
        yield "label", self.label

    def render(self) -> Table:
        grid = Table.grid(padding=0)
        grid.add_column()
        grid.add_row(
            "\\[x]" if self.enabled else "[ ]",
            self.label,
            style=Style(reverse=self.selected),
        )

        return grid

    async def on_click(self, event: events.Click) -> None:
        event.prevent_default().stop()
        await self.emit(ButtonPressed(self))


class FeatureList(View, layout=VerticalLayout, can_focus=True):
    name = 'feature list'
    selection = Reactive(None)

    def __init__(self, feature_set: CompiledFeatureSet, out: ConfigSelection) -> None:
        super().__init__()
        self.feature_set = feature_set
        self.out = out
        self.selection = None

        self.features = []
        for i, feature in enumerate(self.feature_set.features):
            name = feature.name
            if not feature.take_value:
                wg = CheckboxItem(
                    self,
                    label=feature.name,
                    enabled=self.out.values.get(name),
                    selected=False,
                    index=i
                )
                self.features.append(wg)
                self.layout.add(wg)

    @property
    def features_num(self):
        return len(self.features)

    def handle_button_pressed(self, message: ButtonPressed) -> None:
        message.sender.enabled ^= 1
        self.out.values[message.sender.label] = message.sender.enabled

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
        elif event.key == events.Keys.Enter:
            self.handle_button_pressed(ButtonPressed(self.features[self.selection]))


class FeatureSelector(App):
    def __init__(self, feature_set: CompiledFeatureSet, out: ConfigSelection, **kwargs):
        super().__init__(**kwargs)
        self.feature_set = feature_set
        self.out = out

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("q", "quit", "Quit & Save")
        await self.bind("enter", "enter", "Confirm")
        await self.bind("up/down", "up", "Cursor Up/Down")

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""

        # A scrollview to contain the markdown file
        fl = FeatureList(self.feature_set, self.out)

        # Header / footer / dock
        await self.view.dock(Footer(), edge="bottom")

        # Dock the body in the remaining space
        await self.view.dock(fl, edge="right")


def display(feature_set: CompiledFeatureSet) -> ConfigSelection:
    result = ConfigSelection()
    result.values = copy.deepcopy(feature_set.default)
    FeatureSelector.run(title="Select features", feature_set=feature_set, out=result)

    return result
