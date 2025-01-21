from PyQt5 import QtWidgets, QtCore

class Filter(QtWidgets.QWidget):
    state_changed = QtCore.pyqtSignal(str, bool)

    def __init__(self, title, options):
        super().__init__()
        
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        
        self.button = QtWidgets.QPushButton(title)
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.button.toggled.connect(self.toggle)
        self.layout.addWidget(self.button)
        
        self.options_widget = QtWidgets.QWidget()
        self.options_layout = QtWidgets.QVBoxLayout()
        self.options_widget.setLayout(self.options_layout)
        
        self.checkboxes = []
        for option in options:
            checkbox = QtWidgets.QCheckBox(option)
            checkbox.stateChanged.connect(self.checkbox_state_changed)
            self.options_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        
        self.layout.addWidget(self.options_widget)
        self.options_widget.setVisible(True)
        
    def toggle(self, checked):
        self.options_widget.setVisible(checked)

    def checkbox_state_changed(self, state):
        checkbox = self.sender()
        self.state_changed.emit(checkbox.text(), state == QtCore.Qt.Checked)

    def get_checked_status(self):
        status = {}
        for checkbox in self.checkboxes:
            status[checkbox.text()] = checkbox.isChecked()
        return status