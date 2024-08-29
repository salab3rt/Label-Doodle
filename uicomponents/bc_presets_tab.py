from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QCheckBox
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal

class PresetBCPrintTab(QWidget):
    print_signal = pyqtSignal()
    option_signal = pyqtSignal()
    conf_signal = pyqtSignal()
    ortho_btn_signal = pyqtSignal()

    printer_name = None
    option_value = None
    reduced_size = False
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
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
        #self.data_entry.textChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.data_entry)
        
        button_grid_widget = QWidget()

        grid_layout = QGridLayout(button_grid_widget)

        buttons = [
            QPushButton("D2"),
            QPushButton("D3"),
            QPushButton("721"),
            QPushButton("027"),
            QPushButton("D4"),
            QPushButton("D5"),
            QPushButton("722"),
            QPushButton("151"),
            QPushButton("D10"),
            QPushButton("D20"),
            QPushButton("723"),
            QPushButton("203"),
            QPushButton("D100"),
            QPushButton("D1000"),
            QPushButton("724"),
            QPushButton("204"),
            QLabel(),
            QLabel(),
            QPushButton("725"),
            QPushButton("726"),
            # Add more buttons as needed
        ]
        buttons_data = [
            {"text": "D2", "color": "#56855a"},
            {"text": "D3", "color": "#56855a"},
            {"text": "721", "color": "#486684"},
            {"text": "027", "color": "#4c4852"},
            {"text": "D4", "color": "#56855a"},
            {"text": "D5", "color": "#56855a"},
            {"text": "722", "color": "#486684"},
            {"text": "151", "color": "#a35339"},
            {"text": "D10", "color": "#56855a"},
            {"text": "D20", "color": "#56855a"},
            {"text": "723", "color": "#486684"},
            {"text": "203", "color": "#c23232"},
            {"text": "D50", "color": "#56855a"},
            {"text": "D100", "color": "#56855a"},
            {"text": "724", "color": "#486684"},
            {"text": "204", "color": "#c23232"},
            {"text": "D1000", "color": "#56855a"},
            {"text": "003", "color": "#f2692e"},
            {"text": "725", "color": "#486684"},
            {"text": "726", "color": "#23b06f"},
            {"text": "CONF", "color": "#a32e7e"},
            {"text": "ORTHO", "color": "#a32e7e"},
        ]

        for i, data in enumerate(buttons_data):
            if data is not None:
                button = QPushButton(data["text"])
                button.setStyleSheet(f"background-color: {data['color']}; color:'white';")
                grid_layout.addWidget(button, i // 4, i % 4)  # Add buttons in a 2-column grid
                button.button_name = data["text"]
                button.clicked.connect(lambda checked, index=i: self.on_button_clicked(index))
            else:
                spacer = QLabel()
                grid_layout.addWidget(spacer, i // 4, i % 4)

        button_grid_widget.setLayout(grid_layout)

        self.layout.addWidget(button_grid_widget)

        self.print_button = QPushButton("PRINT", self)
        font = QFont("Montserrat", 16, 800)
        self.print_button.setFont(font)
        self.print_button.setStyleSheet("background-color: #212121; color: white; letter-spacing: 2px;")
        self.print_button.clicked.connect(self.on_print_button_click)
        
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance("PRINT")
        self.print_button.setMinimumSize(text_width + 35, fm.height() + 16)
        self.print_button.setMaximumSize(text_width + 35, fm.height() + 18)
        
        self.data_entry.returnPressed.connect(self.on_return_pressed)
        self.layout.addWidget(self.print_button, alignment=Qt.AlignmentFlag.AlignRight)

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
    
    def on_button_clicked(self, index):
        button = self.sender().button_name
        if button == 'CONF':
            self.conf_signal.emit()
        elif button == 'ORTHO':
            self.option_value = ['D2', 'D4', 'D8', 'D16', 'D32', 'D64', 'D128', 'D256', 'D512', 'D1024']
            self.ortho_btn_signal.emit()
        else:
            self.option_value = button
            
            self.option_signal.emit()
            
        self.data_entry.selectAll()
        self.data_entry.setFocus()
        
    def on_print_button_click(self):
        if self.printer_name:
            self.print_signal.emit()
            
        self.data_entry.selectAll()
        self.data_entry.setFocus()
        
    def on_return_pressed(self):
        self.data_entry.selectAll()
        self.data_entry.setFocus()

    def on_text_changed(self, text):
        self.data_entry.setText(text.upper())

    def set_reduced(self, state):
        self.check_reduced = state
        print(self.check_reduced)