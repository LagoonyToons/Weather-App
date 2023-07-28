from types import FunctionType
from PyQt6.QtWidgets import QMessageBox, QApplication
import sys


class Notification():
    def __init__(self, msg: str = None, icon=None, buttons=None):
        self.msg = msg

        self.box = QMessageBox()
        self.box.setWindowTitle('Notification')
        if msg:
            self.box.setText(msg)
        if buttons:
            self.box.setStandardButtons(buttons)
        if icon:
            self.box.setIcon(icon)

    # Set the message to show
    def setMessage(self, msg: str):
        self.box.setText(msg)

    # Send notification to user
    def notify(self):
        self.box.exec()

    # Set a function to run after notification is closed
    def doAfter(self, func: FunctionType):
        self.box.buttonClicked.connect(func)


# To test functionaloty individually
if __name__ == "__main__":
    app = QApplication(sys.argv)

    message = "Test Notification"
    notification = Notification(message)
    notification.notify()

    sys.exit(app.exec())
