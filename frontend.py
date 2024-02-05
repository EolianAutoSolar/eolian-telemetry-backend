from telemetry_core import Service

last = True
# tui interface
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
        print(output + "\033[F"*output.count('\n'), end="", flush=True)