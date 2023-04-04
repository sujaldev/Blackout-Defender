from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import reactive


class Temporary(Static):
    shared_data = reactive("Waiting...")

    def __init__(self, sd: dict):
        super().__init__()
        self.__sd = sd
        self.set_interval(5, self.update_shared_data)

    def update_shared_data(self):
        self.shared_data = str(self.__sd.get("stats", "Waiting for stats..."))

    def watch_stats(self):
        self.update(self.shared_data)

    def render(self):
        return self.shared_data


class TUI(App):
    def __init__(self, shared_data: dict):
        super().__init__()
        self.shared_data = shared_data

    def compose(self) -> ComposeResult:
        yield Temporary(self.shared_data)
