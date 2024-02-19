from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
from .resources import resource_path
from PyQt6 import QtCore

class ClickableLabel(QLabel):
    clicked = QtCore.pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.clicked.emit()
            
    


class TopTitleBar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        #self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)
        
        self.title_label = QLabel("Label Doodle")
        
        icon_path = resource_path("icon.ico")

        self.icon = QPixmap(icon_path)
        self.icon = self.icon.scaled(35, 35, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.title_icon = QLabel("")
        self.title_icon.setPixmap(self.icon)
        
        
        self.layout.addWidget(self.title_icon, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.layout.addStretch()
        
        close_button_icon_path = resource_path("uicomponents/png/close.png")
        self.close_icon = QPixmap(close_button_icon_path)
        self.close_icon = self.close_icon.scaled(25, 25, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.close_label = ClickableLabel("")
        self.close_label.setPixmap(self.close_icon)
        self.layout.addWidget(self.close_label)
        
        self.close_label.clicked.connect(self.close_window)
        
        self.close_label.installEventFilter(self)
        
    def close_window(self):
        self.close_label.setPixmap(self.close_icon)
        self.window().hide()
        
    def eventFilter(self, obj, event):
        if obj == self.close_label:
            #print(event)
            if event.type() == QtCore.QEvent.Type.Enter:
                highlighted_icon = self.close_icon
                highlighted_icon = highlighted_icon.scaled(26, 26, QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                self.close_label.setPixmap(highlighted_icon)
            elif event.type() == QtCore.QEvent.Type.Leave:
                self.close_label.setPixmap(self.close_icon)
            elif event.type() == QtCore.QEvent.Type.MouseButtonPress:
                self.close_label.setPixmap(self.close_icon)
                
        return super().eventFilter(obj, event)