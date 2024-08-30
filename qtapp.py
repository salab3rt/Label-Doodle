import sys, win32gui
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtGui import QIcon, QAction, QFont
from PyQt6.QtCore import Qt, QTimer, QEvent
from labels import label_zebra
from uicomponents.topbar import *
from uicomponents import bc_print_tab, printer_sel_tab, keyboard_hotkeys, bc_history, bc_presets_tab, resources
import qdarktheme


def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

top_windows = []
win32gui.EnumWindows(windowEnumerationHandler, top_windows)
for i in top_windows:
    if "Label Doodle" in i[1]:
        sys.exit()

icon_path = resources.resource_path("icon.ico")

class LabelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        self.hotkey_handler = keyboard_hotkeys.HotkeyManager()
        self.zebra_barcode_printer = label_zebra.ZebraBarcodePrinter()
        
        self.tray_icon.activated.connect(self.on_tray_icon_click)
        self.hotkey_handler.ctrlPressedTwice.connect(self.on_ctrl_pressed_twice)
        self.quick_print_tab.print_signal.connect(self.print_and_add_to_history_list)
        self.printer_select_tab.selected_printer_signal.connect(self.get_printer_name)
        self.preset_bc_tab.print_signal.connect(self.preset_print_and_add_to_history_list)
        self.preset_bc_tab.option_signal.connect(self.replace_extension)
        self.preset_bc_tab.conf_signal.connect(self.print_conf)
        self.preset_bc_tab.ortho_btn_signal.connect(self.print_ortho)

            
        self.quick_print_tab.data_entry.setFocus()
        self.tab_widget.setCurrentIndex(3)
        self.main_window.show()
    
        self.main_window.installEventFilter(self)
        #print(QEvent.Type.FocusOut)
        
    def eventFilter(self, obj, event):
        if obj == self.main_window:
            if event.type() == QEvent.Type.WindowDeactivate and not obj.isActiveWindow():
                self.main_window.showMinimized()
        return super().eventFilter(obj, event)
    
    def on_ctrl_pressed_twice(self):
        if self.main_window.isVisible() and not self.main_window.isMinimized():
            self.main_window.showMinimized()
        else:
            self.on_option_open()
            
    def get_printer_name(self):
        self.selected_printer = self.printer_select_tab.selected_printer
        self.zebra_barcode_printer.set_printer(self.selected_printer)
        
        self.quick_print_tab.printer_name_info.setText(self.selected_printer)
        self.quick_print_tab.printer_name_info.setFont(QFont("Montserrat", 14, 600))
        self.quick_print_tab.printer_name = self.selected_printer
        self.preset_bc_tab.printer_name = self.selected_printer
        self.tab_widget.setCurrentIndex(0)
        
        #print(self.selected_printer)
    
    def print_conf(self):
        data = self.preset_bc_tab.data_entry.text()
        if data:
            for i in range(11, 15, 1):  #exclusive 11-14
                conf_data = str(i) + data
                barcode = self.zebra_barcode_printer.generate_barcode(conf_data, prefix=True, reduced_size=self.preset_bc_tab.reduced_size)
                self.zebra_barcode_printer.print_barcode(barcode)
                self.history_list_tab.add_to_history(conf_data)

    def print_ortho(self):
        data = self.preset_bc_tab.data_entry.text()
        if data:
            for ext in self.preset_bc_tab.option_value:
                barcode = self.check_and_replace_extension(data, ext)
                barcode = self.zebra_barcode_printer.generate_barcode(barcode, reduced_size=self.preset_bc_tab.reduced_size)
                self.zebra_barcode_printer.print_barcode(barcode)

            self.history_list_tab.add_to_history(data)

    def print_and_add_to_history_list(self):
        data = self.quick_print_tab.data_entry.text()
        if data:
            barcode = self.zebra_barcode_printer.generate_barcode(data, reduced_size=self.quick_print_tab.reduced_size)
            self.zebra_barcode_printer.print_barcode(barcode)
            self.history_list_tab.add_to_history(data)
            
    def preset_print_and_add_to_history_list(self):
        data = self.preset_bc_tab.data_entry.text()
        if data:
            self.preset_bc_tab.data_entry.setText(data)
            
            barcode = self.zebra_barcode_printer.generate_barcode(data, reduced_size=self.preset_bc_tab.reduced_size)
            self.zebra_barcode_printer.print_barcode(barcode)
            self.history_list_tab.add_to_history(data)
            #print(data)
        
    def replace_extension(self):
        data = self.preset_bc_tab.data_entry.text()
        #print(f'Data: {data}')
        selected_value = self.preset_bc_tab.option_value
        data = self.check_and_replace_extension(data, selected_value)
        #print(f'altered:{data}')
        self.preset_bc_tab.data_entry.setText(data)
        barcode = self.zebra_barcode_printer.generate_barcode(data, reduced_size=self.preset_bc_tab.reduced_size)
        self.zebra_barcode_printer.print_barcode(barcode)
        self.history_list_tab.add_to_history(data)
        
    def check_and_replace_extension(self, data, selected_value):
        sorted_extensions = sorted(self.zebra_barcode_printer.tube_extensions.keys(), key=len, reverse=True)
        
        extension_found = False
        for extension in sorted_extensions:
            if data.endswith(extension, len(data) - len(extension)):
                extension_found = True
                #data = data[:-len(extension)]
                break
        if extension_found:
            data = data[:-len(extension)] + selected_value
        else:
            data += selected_value
        
        return data

    def init_ui(self):
        
        self.main_window = QMainWindow()
        
        self.main_window.setWindowTitle("Label Doodle")
        
        
        self.setWindowIcon(QIcon(icon_path))
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.setToolTip("Label Doodle")
        
        self.central_widget = QWidget()
        #self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.title_bar = TopTitleBar()
        #self.title_bar.title_label.setFont(QFont(family, 16, 700))
        self.layout.addWidget(self.title_bar)
        
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.quick_print_tab = bc_print_tab.QuickPrintTab()
        self.tab_widget.addTab(self.quick_print_tab, "Print Rápido")
        
        self.preset_bc_tab = bc_presets_tab.PresetBCPrintTab()
        self.tab_widget.addTab(self.preset_bc_tab, "Especiais")
        
        self.history_list_tab = bc_history.HistorySelectTab()
        self.tab_widget.addTab(self.history_list_tab, "Histórico")
        
        self.printer_select_tab = printer_sel_tab.PrinterSelectTab()
        self.tab_widget.addTab(self.printer_select_tab, "Printers")
        
        self.history_list_tab.history_list.itemDoubleClicked.connect(self.on_list_item_double_clicked)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)


        self.set_window_location()

        
        tray_menu = QMenu()
        
        open_action = QAction("Open", self.main_window)
        open_action.triggered.connect(self.on_option_open)
        tray_menu.addAction(open_action)
        
        quit_action = QAction("Quit", self.main_window)
        quit_action.triggered.connect(self.close_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        #self.main_window.setStyleSheet("QMainWindow { border: 1px solid black; border-radius: 10px;}")
    
    def on_tab_changed(self, index):
        # Check if the current tab index is Tab 0
        if index == 0:
            # Select all text in the QLineEdit
            self.quick_print_tab.data_entry.selectAll()
        if index == 1:
            self.preset_bc_tab.data_entry.selectAll()
            self.preset_bc_tab.data_entry.setFocus()
            
    def on_list_item_double_clicked(self, item):
        # Get the text of the double-clicked item
        text = item.text()
        self.quick_print_tab.data_entry.setText(text)
        self.tab_widget.setCurrentIndex(0)
        self.quick_print_tab.data_entry.selectAll()
        

    def set_window_location(self):
        self.main_window.setCentralWidget(self.central_widget)
        
        screen_rect = app.primaryScreen().availableGeometry()
        window_rect = self.main_window.frameGeometry()
        
        x = screen_rect.width() - 400
        y = (screen_rect.height() - 200) / 2
        
        self.main_window.setGeometry(x, int(y), 400, 475)
        self.main_window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        x = screen_rect.width() - window_rect.width()
        y = (screen_rect.height() - window_rect.height()) / 2

        window_rect.setLeft(x)
        window_rect.setTop(int(y))
    
    def on_option_open(self):
        self.main_window.show()
        self.main_window.showMinimized()
        QTimer.singleShot(100, self.activate_and_focus_window)

    def on_tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.main_window.show()
            self.main_window.showMinimized()
            QTimer.singleShot(100, self.activate_and_focus_window)
            
    def activate_and_focus_window(self):
        self.main_window.showNormal()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.tab_widget.setCurrentIndex(0)
        self.quick_print_tab.data_entry.selectAll()
        self.quick_print_tab.data_entry.setFocus()
    
    def close_app(self):
        self.main_window.close()
        sys.exit(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Label Doodle")
    app.setPalette(qdarktheme.load_palette("dark"))
    app.setStyle("Fusion")
    font = QFont("Montserrat", 13, weight=500)
    app.setFont(font)
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon(icon_path))
    
    #font_families = QFontDatabase.families()
    #print(font_families)
    
    label_app = LabelApp()
    
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("Exiting..")
    except Exception as e:
        if e:
            print(f"Exception: {e}")
    finally:
        sys.exit(app.exec())
