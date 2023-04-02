from threading import Thread

from textual.widgets import Static
from textual.reactive import reactive
from textual.app import App, ComposeResult


class ClientStats(Static):
    stats = reactive(0)

    def on_mount(self) -> None:
        self.set_interval(1, self.update_stats)

    def update_stats(self):
        self.stats += 1

    def watch_stats(self, stats: str):
        self.update(str(stats))


class TUI(App):
    def compose(self) -> ComposeResult:
        yield ClientStats()


if __name__ == "__main__":
    tui = TUI()
    tui.run()
