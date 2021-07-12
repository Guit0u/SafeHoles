from PySide2 import QtCore, QtGui, QtWidgets
from matplotlib import numpy as np
import sys
##Fenetre utilisateur

def parse_float(str_value):
    """
    This fuction converts a string to float just like the built-in
    float() function. In addition to "normal" numbers it also handles
    numbers such as 1.2D3 (equivalent to 1.2E3)
    """
    try:
        return float(str_value)
    except ValueError:
        return float(str_value.lower().replace("d", "e"))

class MaFenetre(QtWidgets.QMainWindow):


    def __init__(self, parent=None):
        super().__init__()
        self.points=[]
        self.infopoints=[]
        self.compteur = 0
        self.boutonLire = QtWidgets.QPushButton("enter")
        self.boutonSecurite = QtWidgets.QPushButton("enter")
        self.__champTexte = QtWidgets.QLineEdit("")
        self.__champTexte.setPlaceholderText("exemple.igs")
        self.__champSecurite = QtWidgets.QLineEdit("")
        self.__champSecurite.setPlaceholderText("42")
        self.__unite = QtWidgets.QLabel("millimetri")
        self.__error1 = QtWidgets.QLabel()
        self.__error11 = QtWidgets.QLabel()
        self.__error2 = QtWidgets.QLabel()


        layout1 = QtWidgets.QGridLayout()
        layout1.addWidget(self.__champTexte,0,1)
        layout1.addWidget(self.boutonLire, 1,1 )
        layout1.addWidget(self.boutonSecurite,1,3)
        layout1.addWidget(self.__champSecurite,0,2)
        layout1.addWidget(self.__unite,0,3)
        layout1.addWidget(self.__error1,0,4)
        layout1.addWidget(self.__error11,0,5)
        widget1 = QtWidgets.QWidget()
        widget1.setLayout(layout1)

        self.setCentralWidget(widget1)
        layout2 = QtWidgets.QGridLayout()

        self.__number = QtWidgets.QLabel('1')
        self.__trou = QtWidgets.QLabel('trou')
        self.__coord = QtWidgets.QLabel('wsh')
        self.boutonLire2 = QtWidgets.QPushButton("oui")
        self.__champProfondeur = QtWidgets.QLineEdit("")
        self.__champProfondeur.setPlaceholderText("5")
        self.__labelProfondeur = QtWidgets.QLabel("Depth (mm) :")
        self.__champVitesse = QtWidgets.QLineEdit("")
        self.__champVitesse.setPlaceholderText("5")
        self.__labelVitesse = QtWidgets.QLabel("Speed (mm/s) :")

        layout2.addWidget(self.__champProfondeur, 0, 1)
        layout2.addWidget(self.__labelProfondeur,0,0)
        layout2.addWidget(self.__champVitesse,1,1)
        layout2.addWidget(self.__labelVitesse,1,0)
        layout2.addWidget(self.boutonLire2, 2, 1)
        layout2.addWidget(self.__number, 0, 4)
        layout2.addWidget(self.__trou, 0, 3)
        layout2.addWidget(self.__coord, 0, 5)
        layout2.addWidget(self.__error2, 5, 5)


        self.widget2=QtWidgets.QWidget()
        self.widget2.setLayout(layout2)

        layout3 = QtWidgets.QGridLayout()
        self.widget3 = QtWidgets.QWidget()
        self.widget3.setLayout(layout3)

        self.boutonLire.clicked.connect(self.read)
        self.boutonLire2.clicked.connect(self.FtoPayRespects)
        #self.boutonSecurite.clicked.connect(self.prof)


    def read(self):
        filename = self.__champTexte.text()
        security=self.__champSecurite.text()
        if ',' in security:
            security = float(security.replace(',', '.'))
        try:
            security = float(security)
        except ValueError:
            print('wsh t nul')
            self.__error11.setText('wsh t nul')
            self.__champSecurite.clear()
            return

        try:
            with open(filename,'r') as f:

                param_string = ''
                entity_index = 0
                first_dict_line = True
                first_global_line = True
                first_param_line = True
                global_string = ""
                pointer_dict = {}

                # for line in tqdm(f.readlines(), desc='Reading file'):
                for line in f.readlines():
                    print(line)
                    data = line[:80]
                    id_code = line[72]
                    print(id_code)
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
                                e.add_section(data[0:8], 'entity_type_number')
                                e.add_section(data[8:16], 'parameter_pointer')
                                e.add_section(data[16:24], 'structure')
                                e.add_section(data[24:32], 'line_font_pattern')
                                e.add_section(data[32:40], 'level')
                                e.add_section(data[40:48], 'view')
                                e.add_section(data[48:56], 'transform')
                                e.add_section(data[56:65], 'label_assoc')
                                e.add_section(data[65:72], 'status_number')
                                e.sequence_number = int(data[73:].strip())

                            first_dict_line = False

                        else:
                            if entity_type_number == 116:
                                e.add_section(data[8:16], 'line_weight_number')
                                e.add_section(data[16:24], 'color_number')
                                e.add_section(data[24:32], 'param_line_count')
                                e.add_section(data[32:40], 'form_number')
                                e.add_section(data[56:64], 'entity_label', type='string')
                                e.add_section(data[64:72], 'entity_subs_num')

                                self.points.append(e)
                                pointer_dict.update({e.sequence_number: entity_index})
                                entity_index += 1
                                print(pointer_dict)

                            first_dict_line = True

                    elif id_code == 'P':  # Parameter data
                        for x in pointer_dict:
                            print(x)
                            # Concatenate multiple lines into one string
                        if first_param_line:
                            param_string = data[:64]
                            directory_pointer = int(data[64:72].strip())
                            print(directory_pointer)
                            first_param_line = False
                        else:
                            param_string += data[:64]

                        if param_string.strip()[-1] == record_sep:
                            first_param_line = True
                            param_string = param_string.strip()[:-1]
                            parameters = param_string.split(param_sep)
                            self.points[pointer_dict[directory_pointer]]._add_parameters(parameters)

                    elif id_code == 'T':  # Terminate
                        for e in self.points:
                            print()


            self.setCentralWidget(self.widget2)
            self.__coord.setText(str(self.points[0].coordinate))
        except FileNotFoundError:
            self.__error1.setText('wsh pas fichier')
            self.__champTexte.clear()
            return




    def FtoPayRespects(self):

        if self.compteur<len(self.points):
            self.compteur += 1
            info = self.__champProfondeur.text()
            if ',' in info:
                info=float(info.replace(',', '.'))
            try:
                info=float(info)
            except ValueError:
                print('wsh t nul')
                self.__error2.setText('wsh t nul')
                self.__champProfondeur.clear()
                self.compteur-=1
                return
            self.__champProfondeur.clear()
            self.infopoints.append(info)
            if self.compteur<len(self.points):
                self.__number.setText(str(self.compteur+1))
                self.__coord.setText(str(self.points[self.compteur].coordinate))
            print(self.infopoints)
            if self.compteur==len(self.points):
                self.setCentralWidget(self.widget3)





class Point():
    def __init__(self):
        self.d = dict()
        self.parameters = []

    def add_section(self, string, key, type='int'):
        string = string.strip()
        if type == 'string':
            self.d[key] = string
        else:
            # Status numbers are made of four 2-digit numbers, together making an 8-digit number.
            # It includes spaces, so  0 0 0 0 is a valid 8-digit for which int casting won't work.
            if key == "status_number":
                # Get a list of four 2-digit numbers with spaces removed.
                separated_status_numbers = [string[i:i + 2].replace(' ', '0') for i in range(0, len(string), 2)]

                # Join these status numbers together as a single string.
                status_number_string = ''.join(separated_status_numbers)

                # The string can now be properly cast as an int
                self.d[key] = int(status_number_string)
            elif len(string) > 0:
                self.d[key] = int(string)
            else:
                self.d[key] = None

    def _add_parameters(self, parameters):
        self._x = parse_float(parameters[1])
        self._y = parse_float(parameters[2])
        self._z = parse_float(parameters[3])

    @property
    def x(self):
        """X coordinate"""
        return self._x

    @property
    def y(self):
        """Y coordinate"""
        return self._y

    @property
    def z(self):
        """Z coordinate"""
        return self._z

    @property
    def coordinate(self):
        """Coordinate of the point as a numpy array"""
        return np.array([self._x, self._y, self._z])



app = QtWidgets.QApplication(sys.argv)

window = MaFenetre()
window.show()

app.exec_()