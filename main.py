from PySide2 import QtCore, QtGui, QtWidgets

##Fenetre utilisateur
class MaFenetre(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

    def read(self,filename):
        with open(filename, 'r') as f:
            param_string = ''
            entity_list = []
            entity_index = 0
            first_dict_line = True
            first_global_line = True
            first_param_line = True
            global_string = ""
            pointer_dict = {}

            # for line in tqdm(f.readlines(), desc='Reading file'):
            for line in f.readlines():
                data = line[:80]
                id_code = line[72]

                if id_code == 'S':  # Start
                    desc = line[:72].strip()

                elif id_code == 'G':  # Global
                    global_string += data  # Consolidate all global lines
                    if first_global_line:
                        param_sep = data[2]
                        record_sep = data[6]
                        first_global_line = False

                elif id_code == 'D':  # Directory entry
                    if first_dict_line:
                        entity_type_number = int(data[0:8].strip())
                        if entity_type_number == 116:  # Point
                            e = Point()

class Point