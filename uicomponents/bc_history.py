from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QListWidget
from PyQt6.QtGui import QFont
from PyQt6 import QtCore

class HistorySelectTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        widget_label = QLabel("Histórico de prints:")
        self.layout.addWidget(widget_label)
        self.layout.setContentsMargins(10, 10, 10, 20)
        self.history_list = QListWidget()
        self.history_list.setFont(QFont('Montserrat', 15, 400))
        self.history_list.setContentsMargins(10, 10, 10, 10)
        self.history_list.setStyleSheet("background-color: #212121; color: white; letter-spacing: 2px;")
        
        self.layout.addWidget(self.history_list)
        
    def add_to_history(self, code):
        if not self.history_list.findItems(code, QtCore.Qt.MatchFlag.MatchExactly):
            self.history_list.insertItem(0, code)