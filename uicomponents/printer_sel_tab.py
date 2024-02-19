from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QListWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
import win32print

class PrinterSelectTab(QWidget):
    selected_printer_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        printer_label = QLabel("Escolher impressora:")
        self.layout.addWidget(printer_label)
        self.selected_printer = ''
        
        self.printer_list = QListWidget()
        self.printer_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.get_printers_names()
        
        self.footer = QLabel('Made by salab3rt')
        font = QFont("Montserrat", 9, 500)
        self.footer.setFont(font)
        self.layout.addWidget(self.footer)
        
    def on_selection_changed(self):
        selected_items = self.printer_list.selectedItems()
        if selected_items:
            self.selected_printer = selected_items[0].text()
        self.selected_printer_signal.emit()
        
    def get_printers_names(self):
        ignored_printer_names = {'Microsoft', 'Fax'}
        
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
        for printer in printers:
            if not any(cond in printer[2] for cond in ignored_printer_names):
                item = printer[2]
                self.printer_list.addItem(item)
            
        self.layout.addWidget(self.printer_list)
        