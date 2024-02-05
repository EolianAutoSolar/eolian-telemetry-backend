from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import ProgressBar
from textual.widget import Widget
from refactor import Service
from textual import work

# Class that takes a text and rendered it
class NumberBox(Widget):
    # The reactive object permit the update of the content
    number = reactive(0)

    # The CSS base style of the object
    DEFAULT_CSS = """
        NumberBox {
        column-span: 1;
        width: 1fr;
        height: 1fr;
        content-align: center middle;
        border-top: round white;
        border-title-align: left;
        }
    """

    def render(self) -> str:
        return str(self.number)


# FrontEnd App that reder all the important information to the screen
class FrontEndInterface(App):

    # Definition of the important objects for simpicity
    def __init__(self):
        super().__init__()
        self.SOC = ProgressBar(total=100, show_eta=False, id="soc", classes="data")
        self.KIK = NumberBox()
        self.KIR = NumberBox()
        self.KIT = NumberBox()
        self.BMV = NumberBox()
        self.BMA = NumberBox()
        self.BMT = NumberBox()
        self.KDK = NumberBox()
        self.KDR = NumberBox()
        self.KDT = NumberBox()


    # The CSS style of the APP
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

    # The base order of the objects on the APP screen
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

    # Function that updates the information on de APP when ever the data variable is updated
    def update(self, **component):
        self.SOC.update(progress=component.get("bms_soc", self.SOC.progress))
        self.KIK.number = component.get("kelly_izq_kmh", self.KIK.number)
        self.KIR.number = component.get("kelly_izq_rpm", self.KIR.number)
        self.KIT.number = component.get("kelly_izq_tem", self.KIT.number)
        self.BMV.number = component.get("bms_vol", self.BMV.number)
        self.BMA.number = component.get("bms_amp", self.BMA.number)
        self.BMT.number = component.get("bms_tem", self.BMT.number)
        self.KDK.number = component.get("kelly_der_kmh", self.KDK.number)
        self.KDR.number = component.get("kelly_der_rpm", self.KDR.number)
        self.KDT.number = component.get("kelly_der_tem", self.KDT.number)
        print("id from PS   ", id(self))

# Wrapper for tui interface
class ConsoleVisualization(Service):

    def __init__(self) -> None:
        super().__init__()

    def soc_bar(self, soc) -> str:
        bar_length = 50
        max_soc = 124.0
        percent = soc / max_soc
        complete_length = int(bar_length * percent)
        remaining_length = bar_length - complete_length

        complete_bar = '=' * complete_length
        remaining_bar = '-' * remaining_length

        # Define color codes for the progress bar
        complete_color = '\033[92m'  # Green color for completed part
        remaining_color = '\033[91m'  # Red color for remaining part
        end_color = '\033[0m'  # Reset color after the progress bar

        # Print the progress bar
        return '[' + complete_color + complete_bar + remaining_color + remaining_bar + end_color + f'] {(percent*100):>2.0f}% ({soc:>3} V)'
    
    def main_panel(self, values) -> str:
        return """___________________________________________________
| Kelly izq         BMS            Kelly der      |
| KM/h              Temp           KM/h           | 
| [{kelly_izq_vel:>5.1f} km/h]      [{bms_temp:>3} C]        [{kelly_der_vel:>5.1f} km/h]   | 
|                                                 |
| RPM               Voltaje        RPM            | 
| [{kelly_izq_rpm:>4}]            [{bms_soc:>3} V]        [{kelly_der_rpm:>4}]         |
|                                                 |
| Temp              Corriente      Temp           |
| [{kelly_izq_temp:>3} C]           [{bms_curr:>3} A]        [{kelly_der_temp:>3} C]        |
--------------------------------------------------|""".format(**values)

    def use_data(self, data) -> None:
        panel = self.main_panel(data)
        soc_bar = self.soc_bar(data["bms_soc"])
        # Print the combined text
        output = soc_bar + '\n' + panel
        print(output, end="", flush=True)
        print("\033[F"*output.count('\n'), end="", flush=True)