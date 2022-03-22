from rich.text import Text
from textual import events
from textual.app import App
from textual.widgets import Header, ScrollView
from rich.console import Console
from rich.panel import Panel
from textual_inputs import TextInput

from extract import extract

console = Console()

class OutConsole(ScrollView):
    prev = Text("")

    async def extract(self, text_input):
        pre_y = self.y

        d = extract(text_input)
        if d:
            self.panel = Panel(Text("Etimologia. " + d["etymology"], style="white") + "\n\n" + Text("Definiciones: \n\n" + "\n".join(d["definitions"]), style="white") + "\n\n" + Text("Sinonimos: \n\n" + "\n".join(d["synonyms"]), style="#D3D3D3"), style="bold blue")
        else:
            self.panel = Panel(Text("La palabra no se ha encontrado.", style="bold red"), style="blue")

        await self.update(self.panel)
        self.y = pre_y
        self.animate("y", self.window.virtual_size.height, duration=1, easing="linear")

class InConsole(TextInput):
    def __init__(self, out):
        super(InConsole, self).__init__()
        self.out = out

    async def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            await self.out.extract(self.value)
            self.value = ""

class Dictionary(App):
    async def on_mount(self) -> None:
        output = OutConsole()
        in_put = InConsole(out=output)

        grid = await self.view.dock_grid(edge="left", name="left")
        grid.add_column(fraction=1, name="u")
        grid.add_row(fraction=1, name="top", min_size=3)
        grid.add_row(fraction=1, name="middle", min_size=3)
        grid.add_row(fraction=20, name="bottom")
        grid.add_areas(area1="u,top", area2="u,middle", area3="u,bottom")
        grid.place(area1=Header(style="bold blue"), area2=in_put, area3=output)

if __name__ == "__main__":
    Dictionary.run(title="Diccionario")