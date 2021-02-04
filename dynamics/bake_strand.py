



from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import re
import functools

ABOUT_SCRIPT = "\n" \
               "Latest updates:                \n" \
               "3.02.2021    -start writing   \n" \
               "                               \n" \
               "Created by Andrey Belyaev      \n" \
               "andreikin@mail.ru"

HELP_LABEL = "Select the required character controller and click bake dynamics. \n" \
            "After baking, you can fix problem points manually. "

HELP_TEXT = "\n" \
            "1 Choose the character you want to work with by choosing one of his controllers.\n" \
            "2 Adjust their orientation - the controllers will be oriented in a similar way\n" \
            "3 Make sure the bones are out of the collision objects \n" \
            "4 The root joint must have a parent, to which the system will be attached later\n" \
            "5 Choose 'Create dynanmics sistem'\n" \


class BakeStrand_UI(QMainWindow):
    def __init__(self):
        super(BakeStrand_UI, self).__init__()
        # Window
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Hair strand rigging system")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.__menu_bar()  # help and About script windows
        self.__libel()  # text on top
        self.__option_box()
        #self.__buttons()

    def __menu_bar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)
        menu = QMenu("Help")
        menuBar.addMenu(menu)
        help_action = QAction("Help", self)
        menu.addAction(help_action)
        help_action.triggered.connect(functools.partial(self.text_dialog, "Help"))
        about_script_action = QAction("About script", self)
        menu.addAction(about_script_action)
        about_script_action.triggered.connect(functools.partial(self.text_dialog, "About program"))

    def text_dialog(self, text_type):
        help_dialog = QMessageBox()
        if text_type == "Help":
            help_dialog.setWindowTitle("Help window")
            help_dialog.setText(HELP_TEXT)
        else:
            help_dialog.setWindowTitle("About program")
            help_dialog.setText(ABOUT_SCRIPT)
        help_dialog.setStandardButtons(QMessageBox.Cancel)
        help_dialog.exec_()

    def __libel(self):
        self.help_label = QLabel(HELP_LABEL)
        self.verticalLayout.addWidget(self.help_label)


    def __option_box(self):
        
        self.option_box = QGroupBox("Strand dynamic options:")
        self.option_box_layout = QVBoxLayout(self.option_box)
        
        # slider  
        self.curve_hLayout = QHBoxLayout()
        self.curve_label = QLabel("Strand stiffness :")
        self.curve_hLayout.addWidget(self.curve_label)
        self.curve_horizontal_slider = QSlider()
        self.curve_horizontal_slider.setMinimum(0)
        self.curve_horizontal_slider.setMaximum(10)
        self.curve_horizontal_slider.setSliderPosition(0)
        self.curve_horizontal_slider.setOrientation(Qt.Horizontal)
        self.curve_hLayout.addWidget(self.curve_horizontal_slider)
        
        self.curve_spin_box = QSpinBox()
        self.curve_spin_box.setMinimum(0)
        self.curve_spin_box.setMaximum(10)
        self.curve_spin_box.setValue(0)
        self.curve_hLayout.addWidget(self.curve_spin_box)
        self.curve_horizontal_slider.valueChanged.connect(self.curve_spin_box.setValue)
        self.curve_spin_box.valueChanged.connect(self.curve_horizontal_slider.setValue)
        
        self.stiffness_button = QPushButton(" Set ")
        self.curve_hLayout.addWidget(self.stiffness_button)
        
        self.option_box_layout.addLayout(self.curve_hLayout)
        self.verticalLayout.addWidget(self.option_box)
        
"""      
    def __buttons(self):
        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(2)
        self.bake_selaction_button = QPushButton("Bake_selaction")
        self.button_layout.addWidget(self.bake_selaction_button, 0, 0, 1, 1)
        self.bake_selaction_button.clicked.connect(self.bake_selaction)
        
        self.unbake_selaction_button = QPushButton("Unbake_selaction")
        self.button_layout.addWidget(self.unbake_selaction_button, 1, 0, 1, 1)
        self.unbake_selaction_button.clicked.connect(self.unbake_selaction)
        
        self.bake_all_button = QPushButton("Bake_all")
        self.button_layout.addWidget(self.bake_all_button, 0, 1, 1, 1)
        self.bake_all_button.clicked.connect(self.bake_all)
        
        self.unbake_all_button = QPushButton("Unbake_all")
        self.button_layout.addWidget(self.unbake_all_button, 1, 1, 1, 1)
        self.unbake_all_button.clicked.connect(self.unbake_all)
        
        self.option_box_layout.addLayout(self.button_layout)
        
        self.verticalLayout.addWidget(self.option_box)

""" 
"""  
   
    def is_selaction_dynamics_controller():
        selection = cmds.ls(sl=True)[0]
        prefix = re.sub(r"\d{1,3}_CT$", "", selection)       
    
    
    def bake_selaction(self):
        selection = cmds.ls(sl=True)[0]
        prefix = re.sub(r"\d{1,3}_CT$", "", selection)
        curve_list = self.get_dynamics_curves(selection)
        print("bake_selaction")

    def unbake_selaction(self):
        print("unbake_selaction")

    def bake_all(self):
        print("bake_all")
        curve_list = self.get_dynamics_curves(cmds.ls(sl=True)[0])
        self.bake_curves(curve_list)
        
    def unbake_all(self):
        print("unbake_all")
        
    def bake_curves(self, curve_list):
        cmds.select(curve_list)
        
    def get_referense_prefix(self, obj):
        return re.findall(r"(^[A-Za-z0-9_]*):", obj)[0] 

    def get_dynamics_curves(self, obj):
        char_pfx = self.get_referense_prefix(obj)
        all_follicle = [x for x in cmds.ls(type='follicle') if char_pfx+":" in x]
        dyn_curves = []
        for follicle in all_follicle:
            dyn_curve_shape = cmds.connectionInfo(follicle + ".outCurve", destinationFromSource=True)[0].split('.')[0]
            dyn_curve = cmds.listRelatives(dyn_curve_shape, parent=True)[0]
            dyn_curves.append(dyn_curve)
        return dyn_curves
"""

def bake_strand():
    global bake_win
    try:
        bake_win.deleteLater()
    except NameError:
        pass

    #app = QApplication([])
    bake_win = BakeStrand_UI()
    bake_win.show()
    #app.exec_()

bake_strand()



"""
def get_referense_prefix(obj):
    return re.findall(r"(^[A-Za-z0-9_]*):", obj)[0] 
    
def get_dynamics_curves(obj):
    char_pfx = get_referense_prefix(obj)
    all_follicle = [x for x in cmds.ls(type='follicle') if char_pfx+":" in x]
    dyn_curves = []
    for follicle in all_follicle:
        dyn_curve_shape = cmds.connectionInfo(follicle + ".outCurve", destinationFromSource=True)[0].split('.')[0]
        dyn_curve = cmds.listRelatives(dyn_curve_shape, parent=True)[0]
        dyn_curves.append(dyn_curve)
    return dyn_curves

#obj = cmds.ls(sl=True)[0]
#cmds.select(get_dynamics_curves(obj))


#___________________________________________________________________________


def anim_to_bsh(geo, start, end, del_blds=True, bake_duplicate = False):

    mm.eval("currentTime {} ; ".format(start))

    geoDbl = cmds.duplicate(geo)[0] if bake_duplicate else geo
    targs=[]
    for _ in xrange( start, end+1):
        targs.append(cmds.duplicate(geo)[0])
        mm.eval("playButtonStepForward; ")
    targs.append(geoDbl)

    vBsh = cmds.blendShape (targs[1:],  inBetween=True, origin="world" )[0]
    if del_blds:
        cmds.delete(targs[:-1])

    cmds.setKeyframe(vBsh+".l_dCurv127", value=1, time=end, outTangentType="linear", inTangentType="linear")
    cmds.setKeyframe(vBsh+".l_dCurv127", value=0, time=start, outTangentType="linear", inTangentType="linear")
    mm.eval("currentTime {} ; ".format(start))
    #cmds.setAttr ("liza_ogurcy:hairSystemShape1.simulationMethod", 1)
    #cmds.setAttr ("liza_ogurcy:nucleus1.enable", 0)

    return vBsh


def del_bsp(bsp):
    cmds.delete(bsp)
    #cmds.setAttr ("liza_ogurcy:hairSystemShape1.simulationMethod", 3)
    cmds.setAttr ("liza_ogurcy:nucleus1.enable", 1)
"""

 
 




 









