from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import reactive


class Temporary(Static):
    shared_data = reactive({})

    def __init__(self, shared_data: dict):
        super().__init__()
        self._shared_data = shared_data
        self.set_interval(10, self.update_shared_data)

    def update_shared_data(self):
        self.shared_data = str(self._shared_data)

    def watch_stats(self):
        self.update(str(self.shared_data))


class TUI(App):
    shared_data = reactive({})

    def __init__(self, shared_data: dict):
        super().__init__()
        self._shared_data = shared_data

    def compose(self) -> ComposeResult:
        yield Temporary(self._shared_data)
