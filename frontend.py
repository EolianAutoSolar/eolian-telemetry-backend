

NOT_SAMPLED_YET = -127
# tui interface
class ConsoleVisualization():

    def __init__(self) -> None:
        super().__init__()
        self.id = "TUI"
        view_data = {}
        view_data["kelly_der_rpm"] = NOT_SAMPLED_YET
        view_data["kelly_der_temp"] = NOT_SAMPLED_YET
        view_data["kelly_der_vel"] = NOT_SAMPLED_YET*1.0
        view_data["kelly_izq_rpm"] = NOT_SAMPLED_YET
        view_data["kelly_izq_temp"] = NOT_SAMPLED_YET
        view_data["kelly_izq_vel"] = NOT_SAMPLED_YET*1.0
        view_data["bms_soc"] = NOT_SAMPLED_YET
        view_data["bms_curr"] = NOT_SAMPLED_YET
        view_data["bms_temp"] = NOT_SAMPLED_YET
        self.view_data = view_data

    def soc_bar(self) -> str:
        bar_length = 50
        max_soc = 124.0
        percent = self.view_data["bms_soc"] / max_soc
        complete_length = int(bar_length * percent)
        remaining_length = bar_length - complete_length

        complete_bar = '=' * complete_length
        remaining_bar = '-' * remaining_length

        # Define color codes for the progress bar
        complete_color = '\033[92m'  # Green color for completed part
        remaining_color = '\033[91m'  # Red color for remaining part
        end_color = '\033[0m'  # Reset color after the progress bar
        soc = self.view_data['bms_soc']
        # Print the progress bar
        return '[' + complete_color + complete_bar + remaining_color + remaining_bar + end_color + f'] {(percent*100):>2.0f}% ({soc:>3} V)'
    
    def main_panel(self) -> str:
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
--------------------------------------------------|""".format(**self.view_data)
    def rpm_to_vel(self, rpm):
        return 1.0*rpm #TODO: this formula

    def use_data(self, data) -> None:
        self.view_data["kelly_der_rpm"] = getattr(data, 'kelly_der_rpm', self.view_data['kelly_der_rpm'])
        self.view_data["kelly_der_temp"] = getattr(data, 'kelly_der_rpm', self.view_data['kelly_der_temp'])
        self.view_data["kelly_der_vel"] = self.rpm_to_vel(self.view_data["kelly_der_rpm"])
        self.view_data["kelly_izq_rpm"] = getattr(data, 'kelly_der_rpm', self.view_data['kelly_izq_rpm'])
        self.view_data["kelly_izq_temp"] = getattr(data, 'kelly_der_rpm', self.view_data['kelly_izq_temp'])
        self.view_data["kelly_izq_vel"] = self.rpm_to_vel(self.view_data["kelly_izq_rpm"])
        self.view_data["bms_soc"] = getattr(data, 'kelly_der_rpm', self.view_data['bms_soc'])
        self.view_data["bms_curr"] = getattr(data, 'kelly_der_rpm', self.view_data['bms_curr'])
        self.view_data["bms_temp"] = getattr(data, 'kelly_der_rpm', self.view_data['bms_temp'])
        panel = self.main_panel()
        soc_bar = self.soc_bar()
        # Print the combined text
        output = soc_bar + '\n' + panel
        cursor_up = "\033[F"
        print(output + cursor_up * output.count('\n'), end="", flush=True)
        # print('Frontend visualization {}'.format(data))