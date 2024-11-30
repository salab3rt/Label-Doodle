# Label Doodle - Barcode Generator for Zebra ZPL Prints

## Description

Label Doodle is a quick and easy-to-use desktop application designed to generate barcodes for Zebra ZPL printers. This tool aims to reduce barcode errors in a laboratory setting by enabling fast reprints with minimal interaction. After opening the app by pressing **Ctrl twice**, the user can scan a barcode, and the app will print it right away. If the user presses **Ctrl twice** again or clicks anywhere outside the app, it minimizes to avoid blocking the screen.  

Additionally, you can run the app in CLI mode to preview barcodes before printing without actually sending them to the printer.

### Features

- **Quick Barcode Printing**: Easily scan a barcode and print it immediately.
- **Minimized Mode**: Press **Ctrl twice** or click outside the window to minimize the app when not in use.
- **Zebra ZPL Support**: Specifically designed for Zebra ZPL barcode printers.
- **Printer Selection**: Select a Zebra printer from the available system printers list during initialization.
- **History Tracking**: Keeps a history of scanned barcodes for future reference.
- **CLI Mode**: Run the app in CLI mode to preview barcodes before printing.

## Requirements

Make sure to install the required Python libraries listed in `requirements.txt` before running the application.

```txt
zpl
zebra
pystray
PyQt6
pyqtdarktheme
keyboard
```

## Installation
  1. Clone the repository or download the source code.
  2. Install the required dependencies using pip:
      ```txt
      pip install -r requirements.txt
      ```

  3. Run the application:
     ```txt
     python qtapp.py
     ```

## Usage
### GUI Mode
  1. Select Printer: Upon launching the app, it will automatically detect and allow you to select a Zebra printer from the available system printers list. Make sure you have a Zebra printer installed, as this app uses the ZPL language for barcode printing.

     ![image](https://github.com/user-attachments/assets/40c60407-d563-4a1a-8a35-85e43564f41c)


  3. Open the App: Press Ctrl twice to open the app, or from systray.


     ![image](https://github.com/user-attachments/assets/fe23581f-66a7-4196-adbd-38c667e58a18)

  4. Scan Barcode: Scan the barcode using a barcode scanner, and it will print immediately.


      ![image](https://github.com/user-attachments/assets/c2769356-f1e0-41e9-8beb-13b39d1144f3)

  5. Minimized Mode: Press Ctrl twice again or click outside the window to minimize the app and keep your workspace unobstructed.

### CLI Mode (Preview Only)
You can run the app in CLI mode to preview barcodes without printing.  
This is useful if you just want to verify the barcode output.
Run the app in CLI mode:
```bash
python app.py
```
  ![image](https://github.com/user-attachments/assets/02da3bec-d1b3-4b20-9431-1b815a92ffe7)

  ![image](https://github.com/user-attachments/assets/f49f696f-fcef-4e1e-aec6-86f33eed0c58)

  
### Compiling the Application

For easier distribution without the need for users to install Python, you can compile this application into a single executable file using **auto-py-to-exe**.

 ```bash
 pip install auto-py-to-exe
 ```

