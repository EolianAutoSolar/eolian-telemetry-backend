import can
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import ProgressBar
from textual.widget import Widget

# List used in the data update on main
frontData = [0,0,0,0,0,0,0,0,0,0]

# Class that takes a text and rendered it
class TextBox(Widget):
    # The reactive object permit the update of the content
    text = reactive("NaN")

    # The CSS base style of the object
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


# FrontEnd App that reder all the important information to the screen
class FrontEnd(App):

    # Definition of the important objects for simpicity
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

    # Definition of a reactive object to implement a easy refresh of the screen
    data = reactive([0,0,0,0,0,0,0,0,0,0], always_update=True)

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

# FrontEnd listener -> TODO: Ver que hacerle a esto
# For any can message, it update the FrontEnd data
class Frontend(can.Listener):
    def __init__(self, frontEnd) -> None:
        self.frontEnd = frontEnd
        self.commandIndex = 0
        self.commandPace = 0

    def on_message_received(self, msg: can.Message) -> None:
        # It takes the kelly important data
        if msg.arbitration_id in [0x69, 0xcd]:
            commands = [0x1b, 0x1a, 0x33, 0x37, 0x42, 0x43, 0x44]

            match commands[self.commandIndex]:
                case 0x33:
                    if msg.arbitration_id == 0x69:
                        frontData[3] = msg.data[2]
                    else:
                        frontData[9] = msg.data[2]
                case 0x37:
                    if msg.arbitration_id == 0x69:
                        frontData[1] = msg.data[0]<<8 | msg.data[1]
                        frontData[2] = msg.data[0]<<8 | msg.data[1]
                    else:
                        frontData[7] = msg.data[0]<<8 | msg.data[1]
                        frontData[8] = msg.data[0]<<8 | msg.data[1]


            if self.commandPace == 1:
                self.commandIndex = (self.commandIndex+1) % len(commands)
                self.commandPace = 0
            else:
                self.commandPace = 1

        #It takes the BMS important data
        elif msg.arbitration_id == 0x100:
            frontData[0] = msg.data[0]
            frontData[4] = msg.data[3:5]
            frontData[5] = msg.data[1:3]

        elif msg.arbitration_id == 0x102:
            frontData[6] = msg.data[4]

        #It makes the data update to the FrontEnd App
        self.frontEnd.data = frontData