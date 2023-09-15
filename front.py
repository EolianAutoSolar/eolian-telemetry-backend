from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import ProgressBar
from textual.widget import Widget

class TextBox(Widget):
    text = reactive("NaN")

    DEFAULT_CSS = """
        TextBox {
        column-span: 1;
        width: 1fr;
        height: 1fr;
        content-align: center middle;
        border-top: round white;
        border-title-align: left;
        }
    """

    def render(self) -> str:
        return self.text


class FrontEnd(App):

    def __init__(self):
        super().__init__()
        self.SOC = ProgressBar(total=100, show_eta=False, id="soc", classes="data")
        self.KIK = TextBox()
        self.KIR = TextBox()
        self.KIT = TextBox()
        self.BMV = TextBox()
        self.BMA = TextBox()
        self.BMT = TextBox()
        self.KDK = TextBox()
        self.KDR = TextBox()
        self.KDT = TextBox()

    data = reactive([0,0,0,0,0,0,0,0,0,0], always_update=True)
    CSS = """
        Screen {
        overflow: auto;
        }

        #contentTable {
        layout: grid;
        grid-size: 3 2;
        grid-columns: 1fr 1fr 1fr;
        grid-rows: 1fr 4fr;
        }

        .column {
        layout: grid;
        grid-size: 1 3;
        grid-columns: 1fr;
        grid-rows: 1fr 1fr 1fr;
        border: round white;
        border-title-align: right;
        }

        #soc {
        column-span: 3;
        height: 100%;
        border: round white;
        border-title-align: center;
        }

        #bar {
        width: 1fr;
        height: 1fr;
        padding: 0 1;
        content-align: center middle;
        }

        #percentage {
        content-align: center middle;
        height: 1fr;
        }
        """

    def compose(self) -> ComposeResult:
        with Container(id="contentTable"):
            self.SOC.border_title = "SOC"
            yield self.SOC
            with Container(classes="column") as c1:
                self.KIK.border_title = "<KMH>"
                yield self.KIK
                self.KIR.border_title = "<RPM>"
                yield self.KIR
                self.KIT.border_title = "<Temp>"
                yield self.KIT
                c1.border_title = "Kelly Izquierdo"
            with Container(classes="column") as c2:
                self.BMV.border_title = "<Vol>"
                yield self.BMV
                self.BMA.border_title = "<Amp>"
                yield self.BMA
                self.BMT.border_title = "<Temp>"
                yield self.BMT
                c2.border_title = "BMS"
            with Container(classes="column") as c3:
                self.KDK.border_title = "<KMH>"
                yield self.KDK
                self.KDR.border_title = "<RPM>"
                yield self.KDR
                self.KDT.border_title = "<Temp>"
                yield self.KDT
                c3.border_title = "Kelly Derecho"

    def watch_data(self, old_value, new_value):
        self.SOC.update(progress=new_value[0])
        self.KIK.text = str(new_value[1])
        self.KIR.text = str(new_value[2])
        self.KIT.text = str(new_value[3])
        self.BMV.text = str(new_value[4])
        self.BMA.text = str(new_value[5])
        self.BMT.text = str(new_value[6])
        self.KDK.text = str(new_value[7])
        self.KDR.text = str(new_value[8])
        self.KDT.text = str(new_value[9])
