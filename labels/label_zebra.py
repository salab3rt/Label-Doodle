
from datetime import datetime
import zpl
from zebra import Zebra

class ZebraBarcodePrinter():
    
    _INFO_CHAR_SIZE = 2
    _CODE_HEIGHT = 103
    _CODE_CHAR_SIZE = 5
    _EXTENSION_CHAR_SIZE = 3
    
    tube_prefixes = {
            '11':'CTRL ++ CTRL',
            '12':'CTRL ++ CONF',
            '13':'AMOSTRA ++ CTRL',
            '14':'AMOSTRA ++ CONF'
        }

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
            '030': 'Saliva amostra 030',
            '031': 'Saliva amostra 031',
            '032': 'Saliva amostra 032',
            '033': 'Saliva amostra 033',
            '034': 'Saliva amostra 034',
            '035': 'Saliva amostra 035',
            '981': 'Prova PTGO 981',
            '982': 'Prova PTGO 982',
            '983': 'Prova PTGO 983',
            '984': 'Prova PTGO 984',
            '985': 'Prova PTGO 985',
            '986': 'Prova PTGO 986',
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
            'D2': 'Diluição 1/2',
            'D3': 'Diluição 1/3',
            'D4': 'Diluição 1/4',
            'D5': 'Diluição 1/5',
            'D8': 'Diluição 1/8',
            'D10': 'Diluição 1/10',
            'D16': 'Diluição 1/16',
            'D20': 'Diluição 1/20',
            'D32': 'Diluição 1/32',
            #'D50': 'Diluiç_c3_a3o 1/50',
            'D50': 'Diluição 1/50',
            'D64': 'Diluição 1/64',
            'D100': 'Diluição 1/100',
            'D128': 'Diluição 1/128',
            'D256': 'Diluição 1/256',
            'D512': 'Diluição 1/512',
            'D1000': 'Diluição 1/1000',
            'D1024': 'Diluição 1/1024',
            '999': 'Genérico',
        }
    
    sorted_extensions_keys = sorted(tube_extensions.keys(), key=len, reverse=True)
    
    def __init__(self):
        super().__init__()
        
        self.z = Zebra()

    def generate_barcode(self, data, prefix=False, reduced_size=False):
        
        #print(data)

        self.label = zpl.Label(25,50,8)
        if reduced_size:
            self.label.code+="^BY1"
        
        self.label.change_international_font(character_set=28)
        self.label.field_orientation('N', '0')
        timestamp = datetime.now().strftime("%Y/%m/%d %H:%M")
        
        self.label.origin(2, 1)
        self.label.write_text(
            'CORELAB', 
            char_height=self._INFO_CHAR_SIZE,
            char_width=self._INFO_CHAR_SIZE, 
            line_width=48, 
            justification='L'
        )
        self.label.endorigin()

        self.label.origin(4, 1)
        self.label.write_text(
            timestamp, 
            char_height=self._INFO_CHAR_SIZE, 
            char_width=self._INFO_CHAR_SIZE, 
            line_width=44, 
            justification='R'
        )
        self.label.endorigin()

        self.label.origin(4, 3.5)
        self.label.barcode(
            'C', data, 
            height=self._CODE_HEIGHT, 
            check_digit='Y', 
            orientation='N', 
            mode='A', 
            print_interpretation_line='N'
            )
        self.label.endorigin()

        self.label.origin(0, 17)
        self.label.write_text(
            '^GB400,3,2', 
        )
        self.label.endorigin()

        self.extension = ''
        extension_found = False
        for extension in self.sorted_extensions_keys:
            if data.endswith(extension):
                self.extension = extension
                extension_found = True
                data = data[:-len(extension)]
                break

        if extension_found and not prefix:
            data += self.extension
        #extension = data[len(data)-3:]
        #if extension in self.tube_extensions.keys():
            self.label.origin(4, 18)
            self.label.write_text(
                data[:-len(extension)], 
                char_height=5, 
                char_width=5, 
                line_width=55, 
                justification='L'
            )
            self.label.endorigin()

            self.label.origin(4, 18)
            self.label.write_text(
                extension, 
                char_height=3, 
                char_width=3, 
                line_width=44, 
                justification='R',
            )
            self.label.endorigin()

            self.label.origin(2, 22.5)
            self.label.write_text(
                self.tube_extensions[extension], 
                char_height=2, 
                char_width=2, 
                line_width=44, 
                justification='L'
                )
            self.label.endorigin()

        else:
            self.label.origin(4, 18)
            self.label.write_text(
                data, 
                char_height=5, 
                char_width=5, 
                line_width=55, 
                justification='L'
            )
            self.label.endorigin()

            if prefix:
                self.label.origin(2, 22.5)
                self.label.write_text(
                    self.tube_prefixes[data[:2]], 
                    char_height=2, 
                    char_width=2, 
                    line_width=44, 
                    justification='L'
                    )
                self.label.endorigin()

        #self.label.preview()
        #print(self.label.dumpZPL())
        return self.label.dumpZPL()

    
    def set_printer(self, printer):
        self.z.setqueue(printer)

    def print_barcode(self, barcode):
        #print(barcode)
        try:
            #barcode = barcode.encode('UTF-8')
            #barcode = barcode.encode('UTF-8')
            self.z.output(barcode,
                          encoding='UTF-8'
                          )
            #print(f"Print in {self.z.queue}")
        except Exception as e:
            print(f"Error printing test self.label: {e}")
