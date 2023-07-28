import sys
from typing import Union
from typing_extensions import Literal
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from backend.weather import WeatherData

class CurrentTempWidget(QWidget):
    def __init__(self, weather_data: WeatherData, temp_unit: Union[Literal['F'],Literal['C'], Literal['K']]):
        super().__init__()
        self.wd = weather_data if weather_data != None else WeatherData()
    
        deg = "" if temp_unit == 'K' else u"\N{DEGREE SIGN}"
        self.label = QLabel(self)
        self.label.setText(f'{self.wd.get_current_temp()}{deg} {temp_unit}')

        self.label.setStyleSheet(
            "font-size: 48px;"
            "padding: 25px;")
      


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = CurrentTempWidget(WeatherData(), 'F')
    widget.show()

    sys.exit(app.exec())
