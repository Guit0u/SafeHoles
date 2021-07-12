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

        tabs = QtWidgets.QTabWidget()
        tabs.setTabPosition(QtWidgets.QTabWidget.North)
        tabs.setMovable(False)

        # les boutons

        self.boutonAchat = QtWidgets.QPushButton("no")
        self.boutonVente = QtWidgets.QPushButton("Vendita")

        # Les champs de texte
        self.__champTexte = QtWidgets.QLineEdit("")
        self.__champTexte.setPlaceholderText("Fattura1")
        self.labelMessage = QtWidgets.QLabel("")
        self.labelWarning = QtWidgets.QLabel("")



        layout1 = QtWidgets.QGridLayout()
        layout1.addWidget(self.__champTexte, 1, 1)
        layout1.addWidget(self.labelMessage, 2, 1)
        layout1.addWidget(self.boutonAchat, 3, 2)
        layout1.addWidget(self.boutonVente, 3, 0)
        layout1.addWidget(self.labelWarning, 3, 1)

        widget1 = QtWidgets.QWidget()
        widget1.setLayout(layout1)
        tabs.addTab(widget1, "Inserire una fattura")



        self.setCentralWidget(tabs)
        # disposition widget fenetre




        ##Fonction appelé par le bouton Acquisto
        #self.boutonLire.clicked.connect(self.read(filename="test.igs"))

    def first(self):
        path = Path("../Fatture_Acquisto/" + self.__champTexte.text() + ".pdf")



    def security(self):
        print(self.__champTexte.text())
        print('yes')
        zsecurity=self.__champTexte

    def read(self,filename):
        print('no')
        with open(filename, 'r') as f:

            param_string = ''
            entity_list = []
            entity_index = 0
            first_dict_line = True
            first_global_line = True
            first_param_line = True
            global_string = ""
            pointer_dict = {}

            points=[]

            # for line in tqdm(f.readlines(), desc='Reading file'):
            for line in f.readlines():
                data = line[:80]
                id_code = line[72]
                if id_code == 'P':  # Parameter data
                    if data[:3]=='116':
                        x=int(data[4])
                        y=int(data[7])
                        z=int(data[10])
                        points.append([x,y,z])
            print(points)

        for point in points:
            print('yes')




app = QtWidgets.QApplication(sys.argv)

window = MaFenetre()
window.show()

app.exec_()