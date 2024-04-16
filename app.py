from datetime import datetime
import zpl
from zebra import Zebra
import win32print

z = Zebra()
#print('Printer queues found:',z.getqueues())
#z.print_config_label()

tube_extensions = {
    '000': 'Soro',
    '003': 'Tratamento Eurosorb',
    '100': 'Sangue total EDTA',
    '101': 'Sangue total EDTA',
    '110': 'Sangue total EDTA',
    '190': 'Plasma Citrato',
    '800': 'Urina II',
    '801': 'Urina Química',
    '841': 'Urina Química',
    '300': 'Plasma EDTA-Gel ',
    '030': 'Saliva amostra 1',
    '031': 'Saliva amostra 2',
    '032': 'Saliva amostra 3',
    '033': 'Saliva amostra 4',
    '034': 'Saliva amostra 5',
    '035': 'Saliva amostra 6',
    '981': 'Prova PTGO',
    '982': 'Prova PTGO',
    '983': 'Prova PTGO',
    '984': 'Prova PTGO',
    '985': 'Prova PTGO',
    '986': 'Prova PTGO',
    '050': 'Pós prandial',
    '091': 'Provas',
    '092': 'Provas',
    '093': 'Provas',
    '094': 'Provas',
    '095': 'Provas',
    '096': 'Provas',
    '040': 'Liq. Biológico',
    '020': 'LCR',
    '027': 'LCR',
    '170': 'Fezes',
    '151': 'Fezes',
    '150': 'Urina Minutada',
    '203': 'Acetilcolinest. Eritrocitária',
    '204': 'Imunossupressores',
    '721': 'Macro-ASAT',
    '722': 'Macro-Amilase',
    '723': 'Macro-PRL',
    '724': 'Macro não enzimática',
    '725': 'Macro enzimática',
    '726': 'HDL 2/3',
}

HEADER_HEIGHT = 10
CODE_HEIGHT = 103
FOOTER_HEIGHT = 10

def generate_barcode(data):
    label = zpl.Label(25,50,8)
    label.code+="^BY1"
    label.change_international_font(character_set=28)

    label.field_orientation('N', '2')
    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M")
    #print(timestamp)
    label.origin(2, 1)
    label.write_text('CORELAB', char_height=2, char_width=2, line_width=48, justification='L')
    label.endorigin()

    label.origin(4, 1)
    label.write_text(timestamp, char_height=2, char_width=2, line_width=44, justification='R')
    label.endorigin()

    # Generate the barcode
    label.origin(4, 3.5)
    label.barcode(
        'C', data, 
        height=CODE_HEIGHT, 
        check_digit='Y', 
        orientation='N', 
        mode='A', 
        print_interpretation_line='N'
        )
    label.endorigin()
    
    label.origin(0, 17)
    label.write_text(
        '^GB400,3,2', 
    )
    label.endorigin()

    extension = data[len(data)-3:]
    if extension in tube_extensions.keys():
        label.origin(4, 18)
        label.write_text(
            data[:-3], 
            char_height=5, 
            char_width=5, 
            line_width=55, 
            justification='L'
        )
        label.endorigin()

        label.origin(4, 18)
        label.write_text(
            extension, 
            char_height=3, 
            char_width=3, 
            line_width=44, 
            justification='R',
        )
        label.endorigin()

        label.origin(2, 22.5)
        label.write_text(
            tube_extensions[extension], 
            char_height=2, 
            char_width=2, 
            line_width=44, 
            justification='L'
            )
        label.endorigin()
    
    else:
        label.origin(4, 18)
        label.write_text(data, char_height=5, char_width=5, line_width=55, justification='L')
        label.endorigin()
    
    label.preview()
    print(label.dumpZPL())
    return label.dumpZPL()

def list_printers():
    # Enumerate printers and return a list of printer names
    printers = []
    for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
        printers.append(printer[2])
    return printers

def select_printer():
    # List printers and let the user select one
    printers = list_printers()
    print("Available Printers:")
    for idx, printer in enumerate(printers, start=1):
        print(f"{idx}. {printer}")
    selection = int(input("Select a printer: "))
    
    z.setqueue(printers[selection - 1])

def print_barcode(barcode):
    try:
        z.output(barcode)

        print("Test label printed successfully!")
    except Exception as e:
        print(f"Error printing test label: {e}")

if __name__ == "__main__":
    user_input = input("Enter data for barcode: ")

    bc = generate_barcode(user_input)
    select_printer()

    print_barcode(bc)
    