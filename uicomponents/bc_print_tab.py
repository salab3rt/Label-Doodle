from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal

class QuickPrintTab(QWidget):
    print_signal = pyqtSignal()
    printer_name = None


    def __init__(self):
        super().__init__()
        self.init_ui()
        self.reduced_size = False
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        #self.layout.addStretch(1)
        
        self.data_label = QLabel("Número do código de barras:")
        font = QFont("Montserrat", 14, 500)
        self.data_label.setFont(font)
        self.layout.addWidget(self.data_label)
        
        #self.layout.addStretch(1)
        
        self.data_entry = QLineEdit()
        self.data_entry.setFont(QFont("Montserrat", 26))
        self.data_entry.setMaxLength(20)
        self.data_entry.setStyleSheet("QLineEdit {padding: 5px; letter-spacing: 4px;}")
        self.layout.addWidget(self.data_entry)

        self.print_button = QPushButton("PRINT", self)
        font = QFont("Montserrat", 16, 800)
        self.print_button.setFont(font)
        self.print_button.setStyleSheet("background-color: #212121; color: white; letter-spacing: 2px;")
        self.print_button.clicked.connect(self.on_print_button_click)
        
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance("PRINT")
        self.print_button.setMinimumSize(text_width + 35, fm.height() + 16)
        self.print_button.setMaximumSize(text_width + 35, fm.height() + 18)
        #self.print_button.adjustSize()
        self.data_entry.returnPressed.connect(self.on_return_pressed)
        self.layout.addWidget(self.print_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.footer = QLabel('"CTRL" duas vezes para abrir/fechar a app.')
        font = QFont("Montserrat", 9, 500)
        self.footer.setFont(font)
        self.layout.addWidget(self.footer)
        self.layout.addStretch(2)
        
        self.printer_name_info = QLabel('Selecionar impressora antes de iniciar')
        self.printer_name_info.setWordWrap(True)
        self.printer_name_info.setFont(QFont("Montserrat", 12, 500))
        self.layout.addWidget(self.printer_name_info)
        
        self.layout.addStretch(3)

        self.check_reduced = QCheckBox("Cod. Reduzido", self)
        self.check_reduced.setCheckState(Qt.CheckState.Unchecked)
        self.check_reduced.setTristate(False)
        font = QFont("Montserrat", 10, 400)
        self.check_reduced.setFont(font)
        self.check_reduced.setStyleSheet(" QCheckBox::indicator:checked { border: 2px solid; border-color: #fff; background: #c23232 } \
                                            QCheckBox::indicator:unchecked { border: 2px solid; border-color: #fff; color: #fff; background: #fff; }")
        self.check_reduced.setMaximumSize(150, 20)
        self.check_reduced.setMinimumSize(150, 20)
        self.check_reduced.stateChanged.connect(self.set_reduced)
        self.layout.addWidget(self.check_reduced, alignment=Qt.AlignmentFlag.AlignBottom)
        
        
    def on_print_button_click(self):
        if self.printer_name:
            self.print_signal.emit()
            #print("PRINTED LABEL")
            
        self.data_entry.selectAll()
        self.data_entry.setFocus()
        
    def on_return_pressed(self):
        # Call the same method as clicking the button
        self.on_print_button_click()
        
    def set_reduced(self, state):
        if state == 2:
            self.reduced_size = True
            self.data_entry.setFocus()
        else:
            self.reduced_size = False
            self.data_entry.setFocus()