from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QCompleter
import sys
from backend.weather import WeatherData
import pandas

class SearchboxWidget(QWidget):
    def __init__(self,  weather_data: WeatherData = None):
        super().__init__()

        self.wd = weather_data if weather_data != None else WeatherData()
        # self.label = QLabel(self)
        # self.label.setText("Search box: \n")
        # self.label.setStyleSheet("border: 2px solid black; padding: 4px;")
        # self.label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.names = self.generate_city_list()
        self.completer = QCompleter(self.names)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # Add text field
        self.b = QLineEdit(self)
        # self.b.textEdited.connect(self.updateSuggestions)
        self.b.setCompleter(self.completer)
        # Add button
        self.string = ""
        self.button = QPushButton('Search', self)
        self.button.clicked.connect(self.button_clicked)
        self.button.move(100, 0)

    def button_clicked(self):
        self.string = self.b.text()
        self.wd.get_weather(self.string)
        # self.label.setText("Weather for " + str(self.wd.get_current_humidity()) + ": \n")
        ##flag that everything needs to refresh since wd is changing
    
    # def updateSuggestions(self):
    #     self.names = self.wd.get_city_list(self.b.text())
    #     self.completer.setModel(QStringListModel(self.names))
    #     # self.b.setCompleter(QCompleter(self.names))
    #     # print(self.names)

    def generate_city_list(self):
        with open("suggestions.txt", 'r') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            return lines

# Run file individually to test widget in isolation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = SearchboxWidget()
    widget.show()

    sys.exit(app.exec())
